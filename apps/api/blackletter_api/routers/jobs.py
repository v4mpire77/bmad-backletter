from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models.schemas import JobStatus
from ..services.tasks import get_job


router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str) -> JobStatus:
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="not_found")
    return JobStatus(
        id=job.id,
        job_id=job.id,
        status=job.status,
        analysis_id=job.analysis_id,
        error_reason=job.error_reason,
        created_at=job.created_at,
    )

