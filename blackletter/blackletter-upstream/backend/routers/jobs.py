import logging
from typing import Optional
from uuid import UUID

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..db.session import get_db
from ..jobs import crud
from ..models.schemas import (ContractType, JobCreationResponse,
                              JobResultResponse, JobStatusResponse,
                              Jurisdiction)
from ..services.storage import storage_service
from ..workers.tasks import process_contract

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=JobCreationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a contract for GDPR compliance review",
    description="Upload a contract document and initiate asynchronous GDPR compliance analysis.",
)
async def create_review_job(
    file: UploadFile = File(..., description="Contract document (PDF or DOCX)"),
    contract_type: ContractType = Form(
        ContractType.VENDOR_DPA, description="Type of contract"
    ),
    jurisdiction: Jurisdiction = Form(
        Jurisdiction.EU, description="Applicable jurisdiction"
    ),
    playbook_id: Optional[str] = Form(
        None, description="Custom playbook ID (optional)"
    ),
    db: AsyncSession = Depends(get_db),
):
    """Create a new GDPR compliance review job."""
    try:
        logger.info(f"Processing file upload: {file.filename}")
        file_object_key, file_size = await storage_service.save_file(file)

        job = await crud.create_job_record(
            db=db,
            file_object_key=file_object_key,
            original_filename=file.filename or "unknown",
            file_size=file_size,
            contract_type=contract_type,
            jurisdiction=jurisdiction,
            playbook_id=playbook_id,
        )

        process_contract.delay(str(job.id))
        logger.info(f"Job {job.id} created and dispatched for processing")

        status_url = f"/api/v1/jobs/{job.id}"
        headers = {"Location": status_url}

        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=JobCreationResponse(
                job_id=job.id, status=job.status, created_at=job.created_at
            ).dict(),
            headers=headers,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review job. Please try again.",
        )


@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Get job status",
    description="Retrieve the current status and basic information about a job.",
)
async def get_job_status(job_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get the current status of a job."""
    try:
        job = await crud.get_job_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found",
            )

        return JobStatusResponse(
            job_id=job.id,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
            error_message=job.error_message,
            progress=(
                job.processing_steps_completed[-1]["step"]
                if job.processing_steps_completed
                else None
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving job status {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve job status",
        )


@router.get(
    "/{job_id}/result",
    response_model=JobResultResponse,
    summary="Get job results",
    description="Retrieve the complete analysis results for a completed job.",
)
async def get_job_result(job_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get the complete results of a completed job."""
    try:
        job = await crud.get_job_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found",
            )

        if job.status != schemas.JobStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Job is not completed yet. Current status: {job.status}",
            )

        analysis_result = None
        if job.result:
            analysis_result = schemas.AnalysisResult(**job.result)

        report_url = None
        if job.report_file_key:
            report_url = f"/api/v1/jobs/{job_id}/download"

        return JobResultResponse(
            job_id=job.id,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
            error_message=job.error_message,
            result=analysis_result,
            report_url=report_url,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving job result {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve job result",
        )


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete job and associated data",
    description="Permanently delete a job and all associated data (file, results, etc.).",
)
async def delete_job(job_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a job and all associated data (privacy-by-design)."""
    try:
        job = await crud.get_job_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found",
            )

        if job.file_object_key:
            await storage_service.delete_file(job.file_object_key)
        if job.report_file_key:
            await storage_service.delete_file(job.report_file_key)

        await db.delete(job)
        await db.commit()

        logger.info(f"Job {job_id} and all associated data deleted")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job",
        )
