import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.job import Job
from ..models.schemas import (AnalysisResult, ContractType, JobStatus,
                              Jurisdiction)

logger = logging.getLogger(__name__)


async def create_job_record(
    db: AsyncSession,
    *,
    file_object_key: str,
    original_filename: str,
    file_size: int,
    contract_type: ContractType,
    jurisdiction: Jurisdiction,
    playbook_id: Optional[str] = None,
) -> Job:
    """Creates a new job record in the database."""
    try:
        job = Job(
            file_object_key=file_object_key,
            original_filename=original_filename,
            file_size=file_size,
            contract_type=contract_type,
            jurisdiction=jurisdiction,
            playbook_id=playbook_id,
            status=JobStatus.QUEUED,
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        logger.info(f"Created job record: {job.id}")
        return job

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create job record: {e}")
        raise


async def get_job_by_id(db: AsyncSession, job_id: UUID) -> Optional[Job]:
    """Retrieves a job record by its ID."""
    try:
        result = await db.execute(select(Job).filter(Job.id == job_id))
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Failed to retrieve job {job_id}: {e}")
        raise


async def update_job_status(
    db: AsyncSession,
    job_id: UUID,
    status: JobStatus,
    error_message: Optional[str] = None,
    processing_step: Optional[str] = None,
) -> Optional[Job]:
    """Updates job status and related fields."""
    try:
        result = await db.execute(select(Job).filter(Job.id == job_id))
        job = result.scalars().first()

        if not job:
            return None

        job.status = status
        if error_message:
            job.error_message = error_message
        if status == JobStatus.COMPLETED:
            job.completed_at = datetime.utcnow()
        if processing_step:
            if not job.processing_steps_completed:
                job.processing_steps_completed = []
            job.processing_steps_completed.append(
                {"step": processing_step, "timestamp": datetime.utcnow().isoformat()}
            )

        await db.commit()
        await db.refresh(job)

        logger.info(f"Updated job {job_id} status to {status}")
        return job

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update job {job_id} status: {e}")
        raise


async def update_job_result(
    db: AsyncSession,
    job_id: UUID,
    result: AnalysisResult,
    report_file_key: Optional[str] = None,
    processing_time: Optional[float] = None,
) -> Optional[Job]:
    """Updates job with analysis results."""
    try:
        db_result = await db.execute(select(Job).filter(Job.id == job_id))
        job = db_result.scalars().first()

        if not job:
            return None

        job.result = result.dict()
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()
        if report_file_key:
            job.report_file_key = report_file_key
        if processing_time:
            job.processing_time_seconds = processing_time

        await db.commit()
        await db.refresh(job)

        logger.info(f"Updated job {job_id} with results")
        return job

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update job {job_id} results: {e}")
        raise


async def get_jobs_by_status(
    db: AsyncSession, status: JobStatus, limit: int = 100
) -> List[Job]:
    """Retrieves jobs by status (useful for monitoring)."""
    try:
        result = await db.execute(
            select(Job)
            .filter(Job.status == status)
            .order_by(Job.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Failed to retrieve jobs by status {status}: {e}")
        raise
