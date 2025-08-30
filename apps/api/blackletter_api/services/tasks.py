from __future__ import annotations

import os
import threading
import time
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4

from .storage import analysis_dir, write_analysis_json
from .extraction import run_extraction
from .detector_runner import run_detectors
from ..models.schemas import JobState

logger = logging.getLogger(__name__)


@dataclass
class JobRecord:
    id: str
    status: JobState
    analysis_id: Optional[str]
    error_reason: Optional[str]
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


_JOBS: Dict[str, JobRecord] = {}
_LOCK = threading.Lock()


def new_job(analysis_id: str | None = None) -> str:
    job_id = str(uuid4())
    with _LOCK:
        _JOBS[job_id] = JobRecord(
            id=job_id,
            status=JobState.queued,
            analysis_id=analysis_id,
            error_reason=None,
            created_at=datetime.now(timezone.utc),
        )
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info("New job created and queued", extra=log_extras)
    return job_id


def get_job(job_id: str) -> Optional[JobRecord]:
    with _LOCK:
        return _JOBS.get(job_id)


def set_status(job_id: str, status: JobState, error_reason: str | None = None) -> None:
    with _LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return
        job.status = status
        job.error_reason = error_reason
        now = datetime.now(timezone.utc)
        if status == JobState.running and job.started_at is None:
            job.started_at = now
        if status in (JobState.done, JobState.error):
            job.finished_at = now


def process_job(job_id: str, analysis_id: str, filename: str, size: int) -> None:
    """Orchestration work for the document processing job."""
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info(f"Starting processing for file: {filename}", extra=log_extras)

    try:
        set_status(job_id, JobState.running)
        a_dir = analysis_dir(analysis_id)
        source_path = a_dir / filename
        
        write_analysis_json(analysis_id, filename=filename, size=size)
        
        # Stage 1: Extraction
        t_start_ext = time.time()
        try:
            extraction_path = run_extraction(analysis_id, source_path, a_dir)
            t_end_ext = time.time()
            latency_ms = round((t_end_ext - t_start_ext) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.info("Extraction completed successfully", extra=log_extras)

        except Exception as e:
            t_end_ext = time.time()
            latency_ms = round((t_end_ext - t_start_ext) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.error(f"Extraction failed: {e}", extra=log_extras)
            set_status(job_id, JobState.error, error_reason=f"extraction_failed: {e}")
            return

        # Stage 2: Detection
        t_start_det = time.time()
        try:
            run_detectors(analysis_id, str(extraction_path))
            t_end_det = time.time()
            latency_ms = round((t_end_det - t_start_det) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.info("Detection completed successfully", extra=log_extras)
        except Exception as e:
            t_end_det = time.time()
            latency_ms = round((t_end_det - t_start_det) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.error(f"Detection failed: {e}", extra=log_extras)
            set_status(job_id, JobState.error, error_reason=f"detection_failed: {e}")
            return

        set_status(job_id, JobState.done)
        logger.info("Job processing completed successfully", extra=log_extras)

    except Exception as e:
        logger.error(f"Unhandled error in job processing: {e}", extra=log_extras)
        set_status(job_id, JobState.error, error_reason=str(e))
