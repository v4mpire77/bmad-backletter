from __future__ import annotations

import os
import time
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from redis import Redis

from .storage import analysis_dir, write_analysis_json
from .extraction import run_extraction
from .evidence import build_window
from .exporter import generate_html_export
from .artifacts import (
    record_extraction_artifact,
    record_evidence_artifact,
)
from ..models.schemas import JobState
from .celery_app import celery_app

logger = logging.getLogger(__name__)
@dataclass
class JobRecord:
    id: str
    status: JobState
    analysis_id: Optional[str]
    error_reason: Optional[str]
    created_at: datetime


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


def new_job(analysis_id: str | None = None) -> str:
    job_id = str(uuid4())
    record = {
        "id": job_id,
        "status": JobState.queued.value,
        "analysis_id": analysis_id or "",
        "error_reason": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    redis_client.hset(_job_key(job_id), mapping=record)
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info("New job created and queued", extra=log_extras)
    return job_id


def enqueue_job(
    job_id: str,
    analysis_id: str,
    filename: str,
    size: int,
    backend: str | None = None,
) -> None:
    """Enqueue the document processing job.

    Parameters
    ----------
    job_id, analysis_id, filename, size:
        Identifiers and metadata for the job to enqueue.
    backend:
        Execution backend. ``"sync"`` processes the job immediately within the
        current process, while ``"celery"`` dispatches the job to a Celery
        worker.  If ``None`` the backend defaults to ``"celery"``.

    Notes
    -----
    The previous implementation relied on the ``JOB_SYNC`` environment
    variable.  Explicitly passing the backend makes behaviour clearer and
    simplifies testing.
    """

    chosen = backend or "celery"
    if chosen == "sync":
        process_job(job_id, analysis_id, filename, size)
    elif chosen == "celery":
        process_job.delay(job_id, analysis_id, filename, size)
    else:
        raise ValueError(f"Unknown backend '{chosen}'")


def get_job(job_id: str) -> Optional[JobRecord]:
    data = redis_client.hgetall(_job_key(job_id))
    if not data:
        return None
    return JobRecord(
        id=data["id"],
        status=JobState(data["status"]),
        analysis_id=data.get("analysis_id") or None,
        error_reason=data.get("error_reason") or None,
        created_at=datetime.fromisoformat(data["created_at"]),
    )


def set_status(job_id: str, status: JobState, error_reason: str | None = None) -> None:
    if not redis_client.exists(_job_key(job_id)):
        return
    redis_client.hset(
        _job_key(job_id),
        mapping={"status": status.value, "error_reason": error_reason or ""},
    )


@celery_app.task(name="process_job")
def process_job(job_id: str, analysis_id: str, filename: str, size: int) -> None:
    """Orchestration work for the document processing job."""
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info("Starting job processing", extra=log_extras)

    try:
        set_status(job_id, JobState.running)
        a_dir = analysis_dir(analysis_id)
        source_path = a_dir / filename

        write_analysis_json(analysis_id, filename=filename, size=size)

        # Stage 1: Extraction
        t_start_ext = time.time()
        try:
            extraction_path = run_extraction(analysis_id, source_path, a_dir)
            record_extraction_artifact(
                analysis_id=analysis_id,
                job_id=job_id,
                artifact_path=str(extraction_path),
            )
            t_end_ext = time.time()
            latency_ms = round((t_end_ext - t_start_ext) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.info("Extraction completed successfully", extra=log_extras)

        except Exception as e:
            t_end_ext = time.time()
            latency_ms = round((t_end_ext - t_start_ext) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.error("Extraction failed", extra=log_extras)
            set_status(job_id, JobState.error, error_reason=f"extraction_failed: {e}")
            return

        # Stage 2: Detection (optional if detectors unavailable)
        try:
            from .detector_runner import run_detectors  # Lazy import to avoid hard dependency during tests
        except Exception:
            run_detectors = None  # type: ignore

        if run_detectors is not None:
            t_start_det = time.time()
            try:
                findings = run_detectors(analysis_id, str(extraction_path))
                for f in findings:
                    window = build_window(analysis_id, f.start, f.end)
                    record_evidence_artifact(
                        analysis_id=analysis_id,
                        job_id=job_id,
                        window=window,
                    )
                generate_html_export(analysis_id, findings)
                t_end_det = time.time()
                latency_ms = round((t_end_det - t_start_det) * 1000)
                log_extras["latency_ms"] = latency_ms
                logger.info("Detection completed successfully", extra=log_extras)
            except Exception as e:
                t_end_det = time.time()
                latency_ms = round((t_end_det - t_start_det) * 1000)
                log_extras["latency_ms"] = latency_ms
                logger.error("Detection failed", extra=log_extras)
                set_status(job_id, JobState.error, error_reason=f"detection_failed: {e}")
                return
        else:
            logger.info("Detection skipped: detectors unavailable", extra=log_extras)

        set_status(job_id, JobState.done)
        logger.info("Job processing completed successfully", extra=log_extras)

    except Exception as e:
        logger.error("Unhandled error in job processing", extra=log_extras)
        set_status(job_id, JobState.error, error_reason=str(e))
