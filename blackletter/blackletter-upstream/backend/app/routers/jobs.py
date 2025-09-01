"""
Blackletter GDPR Processor - Jobs API Router
Context Engineering Framework v2.0.0 Compliant
Implements 202 Accepted pattern for async job processing
"""
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
import aiofiles
import tempfile
import os

from app.models.schemas import (
    JobCreateResponse, JobStatus, JobResult, JobStatusEnum,
    ErrorResponse
)
from app.services.job_service import job_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=JobCreateResponse, status_code=202)
async def create_job(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
) -> JSONResponse:
    """
    Create new GDPR analysis job.
    Returns 202 Accepted with Location header pointing to status endpoint.
    
    Following API design memory requirement for 202 Accepted pattern.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        # Check file size
        if file.size and file.size > settings.max_upload_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.max_upload_size} bytes"
            )
        
        # Check file type
        if file.content_type:
            file_extension = file.filename.split('.')[-1].lower()
            if file_extension not in settings.allowed_file_types:
                raise HTTPException(
                    status_code=415,
                    detail=f"Unsupported file type. Allowed: {', '.join(settings.allowed_file_types)}"
                )
        
        # Create job
        job_id = await job_service.create_job(
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            file_size=file.size or 0
        )
        
        # Store file temporarily and queue analysis
        background_tasks.add_task(process_uploaded_file, job_id, file)
        
        # Build location URL for status checking
        base_url = str(request.base_url).rstrip('/')
        location = f"{base_url}/api/v1/jobs/{job_id}/status"
        
        # Create response following 202 Accepted pattern
        response_data = JobCreateResponse(
            job_id=job_id,
            status=JobStatusEnum.PENDING,
            message="Job created successfully",
            location=location
        )
        
        logger.info(f"Created job {job_id} for file: {file.filename}")
        
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
        logger.error(f"Error creating job: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create analysis job")


@router.get("/{job_id}/status", response_model=JobStatus)
async def get_job_status(job_id: str) -> JobStatus:
    """
    Get current job processing status.
    Used for polling job progress after 202 Accepted response.
    """
    try:
        job_status = await job_service.get_job_status(job_id)
        
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        logger.debug(f"Status check for job {job_id}: {job_status.status}")
        return job_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get job status")


@router.get("/{job_id}/result", response_model=JobResult)
async def get_job_result(job_id: str) -> JobResult:
    """
    Get analysis results for completed job.
    Returns 404 if job not found, 202 if still processing.
    """
    try:
        # First check if job exists
        job_status = await job_service.get_job_status(job_id)
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # If still processing, return 202 with status info
        if job_status.status in [JobStatusEnum.PENDING, JobStatusEnum.PROCESSING]:
            response_data = {
                "message": f"Job still {job_status.status.value}",
                "status": job_status.status,
                "progress": job_status.progress
            }
            return JSONResponse(status_code=202, content=response_data)
        
        # Get completed result
        result = await job_service.get_job_result(job_id)
        if not result:
            raise HTTPException(status_code=404, detail="Job result not found")
        
        logger.debug(f"Retrieved result for job {job_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job result {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get job result")


@router.delete("/{job_id}")
async def cancel_job(job_id: str) -> dict:
    """
    Cancel a pending or processing job.
    Returns 404 if job not found, 409 if already completed.
    """
    try:
        # Check if job exists
        job_status = await job_service.get_job_status(job_id)
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Check if job can be cancelled
        if job_status.status in [JobStatusEnum.COMPLETED, JobStatusEnum.FAILED, JobStatusEnum.CANCELLED]:
            raise HTTPException(
                status_code=409,
                detail=f"Cannot cancel job with status: {job_status.status}"
            )
        
        # Cancel the job
        cancelled = await job_service.cancel_job(job_id)
        if not cancelled:
            raise HTTPException(status_code=500, detail="Failed to cancel job")
        
        logger.info(f"Cancelled job {job_id}")
        return {"message": "Job cancelled successfully", "job_id": job_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to cancel job")


@router.get("/", response_model=List[JobStatus])
async def list_jobs(limit: int = 50) -> List[JobStatus]:
    """
    List recent jobs for monitoring and debugging.
    Limited to prevent performance issues.
    """
    try:
        if limit > 100:
            limit = 100  # Enforce maximum limit
        
        jobs = await job_service.list_jobs(limit=limit)
        logger.debug(f"Listed {len(jobs)} jobs")
        return jobs
        
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list jobs")


@router.get("/stats")
async def get_job_statistics() -> dict:
    """
    Get job processing statistics for monitoring.
    Development endpoint - disable in production.
    """
    if not settings.is_development:
        raise HTTPException(status_code=404, detail="Endpoint not available in production")
    
    try:
        stats = await job_service.get_statistics()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting job statistics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get statistics")


async def process_uploaded_file(job_id: str, file: UploadFile):
    """
    Background task to process uploaded file.
    Triggers Celery task for actual analysis.
    """
    try:
        # Update job status to processing
        await job_service.update_job_status(
            job_id, 
            JobStatusEnum.PROCESSING, 
            progress=0.1,
            message="Processing uploaded file"
        )
        
        # Save file temporarily
        temp_file_path = None
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
                temp_file_path = temp_file.name
                
                # Read and save file content
                content = await file.read()
                temp_file.write(content)
                temp_file.flush()
            
            logger.info(f"Saved uploaded file for job {job_id}: {temp_file_path}")
            
            # Import and trigger Celery task
            from workers.celery_app import analyze_contract_task
            
            # Queue analysis task
            task = analyze_contract_task.delay(job_id, temp_file_path, file.filename)
            
            logger.info(f"Queued analysis task {task.id} for job {job_id}")
            
        finally:
            # Cleanup temporary file after task is queued
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.debug(f"Cleaned up temporary file: {temp_file_path}")
                except Exception as cleanup_error:
                    logger.warning(f"Failed to cleanup temp file {temp_file_path}: {cleanup_error}")
                    
    except Exception as e:
        logger.error(f"Error processing uploaded file for job {job_id}: {str(e)}", exc_info=True)
        
        # Mark job as failed
        await job_service.complete_job(
            job_id,
            analysis_result=None,
            error=f"File processing failed: {str(e)}"
        )