from __future__ import annotations
import logging
import time

from fastapi import APIRouter, HTTPException

from ..models.schemas import JobStatus
from ..services.tasks import get_job

logger = logging.getLogger(__name__)
router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str) -> JobStatus:
    request_start = time.time()
    
    job = get_job(job_id)
    if not job:
        request_time = round((time.time() - request_start) * 1000)
        logger.warning("Job not found", extra={
            "job_id": job_id,
            "request_latency_ms": request_time
        })
        raise HTTPException(status_code=404, detail="not_found")
    
    request_time = round((time.time() - request_start) * 1000)
    logger.info("Job status retrieved", extra={
        "job_id": job_id,
        "analysis_id": job.analysis_id,
        "status": job.status.value,
        "request_latency_ms": request_time
    })
    
    return JobStatus(
        id=job.id,
        job_id=job.id,
        status=job.status,
        analysis_id=job.analysis_id,
        error_reason=job.error_reason,
        created_at=job.created_at,
    )

