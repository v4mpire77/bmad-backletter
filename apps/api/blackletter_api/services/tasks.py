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
from .detector_runner import run_detectors
from .evidence import build_window
from .exporter import generate_html_export
from .artifacts import (
    record_extraction_artifact,
    record_evidence_artifact,
)
from ..models.schemas import JobState
from .celery_app import celery_app

logger = logging.getLogger(__name__)


def log_transition(
    *,
    job_id: str,
    state: str,
    tenant_id: str | None = None,
    attempt: int = 1,
    queued_at: datetime | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
    duration_ms: int | None = None,
    error_type: str | None = None,
    error_msg: str | None = None,
) -> None:
    logger.info(
        f"task_{state}",
        extra={
            "job_id": job_id,
            "tenant_id": tenant_id,
            "state": state,
            "attempt": attempt,
            "queued_at": queued_at.isoformat() if queued_at else None,
            "started_at": started_at.isoformat() if started_at else None,
            "finished_at": finished_at.isoformat() if finished_at else None,
            "duration_ms": duration_ms,
            "error_type": error_type,
            "error_msg": error_msg,
        },
    )
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
    log_transition(
        job_id=job_id,
        state="queued",
        tenant_id=None,
        attempt=0,
        queued_at=datetime.fromisoformat(record["created_at"]),
    )
    return job_id


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
    job = get_job(job_id)
    queued_at = job.created_at if job else None
    started_at = datetime.now(timezone.utc)
    log_transition(
        job_id=job_id,
        state="start",
        queued_at=queued_at,
        started_at=started_at,
    )

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
        except Exception as e:
            t_end_ext = time.time()
            duration_ms = round((t_end_ext - t_start_ext) * 1000)
            log_transition(
                job_id=job_id,
                state="error",
                queued_at=queued_at,
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
                duration_ms=duration_ms,
                error_type=type(e).__name__,
                error_msg=str(e),
            )
            set_status(job_id, JobState.error, error_reason=f"extraction_failed: {e}")
            return

        # Stage 2: Detection
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
        except Exception as e:
            t_end_det = time.time()
            duration_ms = round((t_end_det - t_start_det) * 1000)
            log_transition(
                job_id=job_id,
                state="error",
                queued_at=queued_at,
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
                duration_ms=duration_ms,
                error_type=type(e).__name__,
                error_msg=str(e),
            )
            set_status(job_id, JobState.error, error_reason=f"detection_failed: {e}")
            return

        set_status(job_id, JobState.done)
        finished_at = datetime.now(timezone.utc)
        duration_ms = round((finished_at - started_at).total_seconds() * 1000)
        log_transition(
            job_id=job_id,
            state="success",
            queued_at=queued_at,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=duration_ms,
        )

    except Exception as e:
        finished_at = datetime.now(timezone.utc)
        duration_ms = round((finished_at - started_at).total_seconds() * 1000)
        log_transition(
            job_id=job_id,
            state="error",
            queued_at=queued_at,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_msg=str(e),
        )
        set_status(job_id, JobState.error, error_reason=str(e))
