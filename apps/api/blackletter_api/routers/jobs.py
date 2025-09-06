"""
Enhanced Jobs API Router with 202 Accepted Pattern
Integrated from v4mpire77/blackletter for async job processing
Context Engineering Framework v2.0.0 Compliant
"""
from __future__ import annotations

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from ..models.schemas import JobStatus, JobCreateResponse, JobState
from ..services.tasks import get_job, create_contract_analysis_job

logger = logging.getLogger(__name__)

router = APIRouter(tags=["jobs"])


@router.post("/", response_model=JobCreateResponse, status_code=202)
async def create_job(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
) -> JSONResponse:
    """
    Create new GDPR analysis job with 202 Accepted pattern.
    Returns 202 Accepted with Location header pointing to status endpoint.
    
    Enhanced from v4mpire77/blackletter integration for async processing.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size and file.size > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {max_size} bytes"
            )
        
        # Check file type
        allowed_types = ["pdf", "docx", "doc"]
        if file.filename:
            file_extension = file.filename.split('.')[-1].lower()
            if file_extension not in allowed_types:
                raise HTTPException(
                    status_code=415,
                    detail=f"Unsupported file type. Allowed: {', '.join(allowed_types)}"
                )
        
        # Create job and queue analysis
        job_id = await create_contract_analysis_job(
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            file_content=await file.read()
        )
        
        # Build location URL for status checking
        base_url = str(request.base_url).rstrip('/')
        location = f"{base_url}/api/jobs/{job_id}"
        
        # Create response following 202 Accepted pattern
        response_data = JobCreateResponse(
            job_id=job_id,
            status=JobState.queued,
            message="Analysis job created successfully",
            location=location
        )
        
        logger.info(f"Created analysis job {job_id} for file: {file.filename}")
        
        # Return 202 with Location header
        response = JSONResponse(
            status_code=202,
            content=response_data.model_dump(),
            headers={"Location": location}
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analysis job: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create analysis job")


@router.get("/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str) -> JobStatus:
    """Get job status with enhanced error handling."""
    job = get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Job not found"},
        )
    return JobStatus(
        id=job.id,
        job_id=job.id,
        status=job.status,
        analysis_id=job.analysis_id,
        error_reason=job.error_reason,
        created_at=job.created_at,
    )


# Legacy compatibility endpoint
@router.get("/jobs/{job_id}", response_model=JobStatus)
def get_job_status_legacy(job_id: str) -> JobStatus:
    """Legacy endpoint for backward compatibility."""
    return get_job_status(job_id)

