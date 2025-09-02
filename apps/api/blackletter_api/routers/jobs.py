from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ..models.schemas import JobStatus
from ..services.tasks import get_job
import logging

logger = logging.getLogger(__name__)


router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str, request: Request) -> JobStatus:
    logger.info(
        "job_status_request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "tenant_id": getattr(request.state, "tenant_id", None),
            "job_id": job_id,
        },
    )
    job = get_job(job_id)
    if not job:
        logger.info(
            "job_status_response",
        extra={"job_id": job_id, "status_code": 404, "state": "not_found"},
        )
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Job not found"},
        )
    logger.info(
        "job_status_response",
        extra={"job_id": job_id, "status_code": 200, "state": job.status.value},
    )
    return JobStatus(
        id=job.id,
        job_id=job.id,
        status=job.status,
        analysis_id=job.analysis_id,
        error_reason=job.error_reason,
        created_at=job.created_at,
    )

