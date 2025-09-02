from __future__ import annotations

import os
import time
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from .storage import analysis_dir, write_analysis_json
from .extraction import run_extraction
from .detector_runner import run_detectors
from ..database import SessionLocal
from ..models.entities import Job
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


def new_job(db: Session, analysis_id: str | None = None) -> str:
    job = Job(analysis_id=analysis_id, status=JobState.queued.value)
    db.add(job)
    db.commit()
    db.refresh(job)
    log_extras = {"job_id": str(job.id), "analysis_id": analysis_id}
    logger.info("New job created and queued", extra=log_extras)
    return str(job.id)


def get_job(db: Session, job_id: str) -> Optional[JobRecord]:
    job = db.get(Job, job_id)
    if job is None:
        return None
    return JobRecord(
        id=str(job.id),
        status=JobState(job.status),
        analysis_id=str(job.analysis_id) if job.analysis_id else None,
        error_reason=job.error_reason,
        created_at=job.created_at,
    )


def set_status(
    db: Session, job_id: str, status: JobState, error_reason: str | None = None
) -> None:
    job = db.get(Job, job_id)
    if job is None:
        return
    job.status = status.value
    job.error_reason = error_reason
    db.commit()


@celery_app.task(name="process_job")
def process_job(job_id: str, analysis_id: str, filename: str, size: int) -> None:
    """Orchestration work for the document processing job."""
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info(f"Starting processing for file: {filename}", extra=log_extras)

    db = SessionLocal()
    try:
        set_status(db, job_id, JobState.running)
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
            set_status(db, job_id, JobState.error, error_reason=f"extraction_failed: {e}")
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
            set_status(db, job_id, JobState.error, error_reason=f"detection_failed: {e}")
            return

        set_status(db, job_id, JobState.done)
        logger.info("Job processing completed successfully", extra=log_extras)

    except Exception as e:
        logger.error(f"Unhandled error in job processing: {e}", extra=log_extras)
        set_status(db, job_id, JobState.error, error_reason=str(e))
    finally:
        db.close()
