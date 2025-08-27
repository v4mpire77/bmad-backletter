from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4

from .storage import analysis_dir, write_analysis_json
from .extraction import run_extraction
from ..models.schemas import JobState


@dataclass
class JobRecord:
    id: str
    status: JobState
    analysis_id: Optional[str]
    error_reason: Optional[str]
    created_at: datetime


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


def process_job(job_id: str, analysis_id: str, filename: str, size: int) -> None:
    """Simulate orchestration work for MVP.

    For tests or local dev, if JOB_SYNC=1 is set in env, run synchronously.
    """
    try:
        set_status(job_id, JobState.running)
        a_dir = analysis_dir(analysis_id)
        source_path = a_dir / filename
        # Persist analysis metadata
        write_analysis_json(analysis_id, filename=filename, size=size)
        # Run extraction (PDF/DOCX)
        try:
            run_extraction(analysis_id, source_path, a_dir)
        except Exception as e:
            set_status(job_id, JobState.error, error_reason=f"extraction_failed: {e}")
            return
        set_status(job_id, JobState.done)
    except Exception as e:
        set_status(job_id, JobState.error, error_reason=str(e))
