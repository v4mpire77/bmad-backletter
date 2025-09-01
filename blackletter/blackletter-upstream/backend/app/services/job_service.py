"""
Blackletter GDPR Processor - Job Service
Context Engineering Framework v2.0.0 Compliant
Manages async job processing with in-memory store for MVP
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from uuid import uuid4

from app.models.schemas import (
    JobStatus, JobResult, JobStatusEnum, AnalysisResult,
    generate_job_id
)

logger = logging.getLogger(__name__)


class JobService:
    """
    Async job management service.
    Uses in-memory storage for MVP - replace with database in production.
    """
    
    def __init__(self):
        """Initialize job service with in-memory stores."""
        self._jobs: Dict[str, Dict] = {}
        self._results: Dict[str, JobResult] = {}
        self._cleanup_interval = 3600  # 1 hour cleanup interval
        self._job_timeout = 300  # 5 minutes default timeout
        self._max_jobs = 1000  # Maximum jobs to keep in memory
        
        logger.info("JobService initialized with in-memory storage")
    
    async def create_job(self, filename: str, content_type: str, file_size: int) -> str:
        """
        Create a new analysis job.
        
        Args:
            filename: Uploaded filename
            content_type: File MIME type
            file_size: File size in bytes
            
        Returns:
            job_id: Unique job identifier
        """
        job_id = generate_job_id()
        
        job_data = {
            "job_id": job_id,
            "status": JobStatusEnum.PENDING,
            "progress": 0.0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "filename": filename,
            "content_type": content_type,
            "file_size": file_size,
            "message": "Job created successfully"
        }
        
        self._jobs[job_id] = job_data
        
        logger.info(f"Created job {job_id} for file: {filename}")
        
        # Cleanup old jobs if needed
        await self._cleanup_old_jobs()
        
        return job_id
    
    async def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        """
        Get current job status.
        
        Args:
            job_id: Job identifier
            
        Returns:
            JobStatus or None if not found
        """
        job_data = self._jobs.get(job_id)
        
        if not job_data:
            logger.warning(f"Job {job_id} not found")
            return None
        
        return JobStatus(
            job_id=job_data["job_id"],
            status=job_data["status"],
            progress=job_data["progress"],
            created_at=job_data["created_at"],
            updated_at=job_data["updated_at"],
            message=job_data.get("message")
        )
    
    async def update_job_status(
        self, 
        job_id: str, 
        status: JobStatusEnum, 
        progress: float = None, 
        message: str = None
    ) -> bool:
        """
        Update job status and progress.
        
        Args:
            job_id: Job identifier
            status: New job status
            progress: Progress value (0.0 - 1.0)
            message: Optional status message
            
        Returns:
            True if updated, False if job not found
        """
        job_data = self._jobs.get(job_id)
        
        if not job_data:
            logger.warning(f"Cannot update job {job_id} - not found")
            return False
        
        job_data["status"] = status
        job_data["updated_at"] = datetime.utcnow()
        
        if progress is not None:
            job_data["progress"] = max(0.0, min(1.0, progress))
        
        if message is not None:
            job_data["message"] = message
        
        logger.debug(f"Updated job {job_id}: {status} ({job_data['progress']:.1%})")
        
        return True
    
    async def complete_job(
        self, 
        job_id: str, 
        analysis_result: Optional[AnalysisResult] = None, 
        error: str = None
    ) -> bool:
        """
        Mark job as completed with results or error.
        
        Args:
            job_id: Job identifier
            analysis_result: Analysis results if successful
            error: Error message if failed
            
        Returns:
            True if completed, False if job not found
        """
        job_data = self._jobs.get(job_id)
        
        if not job_data:
            logger.warning(f"Cannot complete job {job_id} - not found")
            return False
        
        completed_at = datetime.utcnow()
        processing_time = (completed_at - job_data["created_at"]).total_seconds()
        
        # Determine final status
        final_status = JobStatusEnum.COMPLETED if analysis_result else JobStatusEnum.FAILED
        
        # Update job status
        job_data["status"] = final_status
        job_data["progress"] = 1.0
        job_data["updated_at"] = completed_at
        job_data["message"] = "Analysis completed successfully" if analysis_result else error
        
        # Store result
        job_result = JobResult(
            job_id=job_id,
            status=final_status,
            analysis=analysis_result,
            error=error,
            created_at=job_data["created_at"],
            completed_at=completed_at,
            processing_time=processing_time
        )
        
        self._results[job_id] = job_result
        
        logger.info(f"Completed job {job_id}: {final_status} in {processing_time:.2f}s")
        
        return True
    
    async def get_job_result(self, job_id: str) -> Optional[JobResult]:
        """
        Get job result if completed.
        
        Args:
            job_id: Job identifier
            
        Returns:
            JobResult or None if not found/not completed
        """
        result = self._results.get(job_id)
        
        if not result:
            # Check if job exists and is still processing
            job_data = self._jobs.get(job_id)
            if job_data and job_data["status"] in [JobStatusEnum.PENDING, JobStatusEnum.PROCESSING]:
                logger.debug(f"Job {job_id} not ready - still processing")
                return None
            else:
                logger.warning(f"Job result {job_id} not found")
                return None
        
        return result
    
    async def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a pending or processing job.
        
        Args:
            job_id: Job identifier
            
        Returns:
            True if cancelled, False if not found or already completed
        """
        job_data = self._jobs.get(job_id)
        
        if not job_data:
            return False
        
        # Can only cancel pending or processing jobs
        if job_data["status"] not in [JobStatusEnum.PENDING, JobStatusEnum.PROCESSING]:
            logger.warning(f"Cannot cancel job {job_id} - status: {job_data['status']}")
            return False
        
        job_data["status"] = JobStatusEnum.CANCELLED
        job_data["updated_at"] = datetime.utcnow()
        job_data["message"] = "Job cancelled by user"
        
        logger.info(f"Cancelled job {job_id}")
        return True
    
    async def list_jobs(self, limit: int = 50) -> List[JobStatus]:
        """
        List recent jobs.
        
        Args:
            limit: Maximum number of jobs to return
            
        Returns:
            List of JobStatus objects
        """
        # Sort jobs by creation time (newest first)
        sorted_jobs = sorted(
            self._jobs.values(),
            key=lambda x: x["created_at"],
            reverse=True
        )
        
        job_statuses = []
        for job_data in sorted_jobs[:limit]:
            job_statuses.append(JobStatus(
                job_id=job_data["job_id"],
                status=job_data["status"],
                progress=job_data["progress"],
                created_at=job_data["created_at"],
                updated_at=job_data["updated_at"],
                message=job_data.get("message")
            ))
        
        return job_statuses
    
    async def _cleanup_old_jobs(self):
        """Clean up old completed jobs to prevent memory leaks."""
        try:
            current_time = datetime.utcnow()
            cleanup_threshold = current_time - timedelta(seconds=self._cleanup_interval)
            
            # Remove old completed jobs
            jobs_to_remove = []
            for job_id, job_data in self._jobs.items():
                if (job_data["status"] in [JobStatusEnum.COMPLETED, JobStatusEnum.FAILED, JobStatusEnum.CANCELLED] 
                    and job_data["updated_at"] < cleanup_threshold):
                    jobs_to_remove.append(job_id)
            
            # Enforce maximum job limit
            if len(self._jobs) > self._max_jobs:
                # Remove oldest jobs beyond limit
                sorted_jobs = sorted(
                    self._jobs.items(),
                    key=lambda x: x[1]["created_at"]
                )
                
                excess_count = len(self._jobs) - self._max_jobs
                for job_id, _ in sorted_jobs[:excess_count]:
                    jobs_to_remove.append(job_id)
            
            # Perform cleanup
            for job_id in jobs_to_remove:
                self._jobs.pop(job_id, None)
                self._results.pop(job_id, None)
            
            if jobs_to_remove:
                logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
                
        except Exception as e:
            logger.error(f"Error during job cleanup: {e}")
    
    async def get_statistics(self) -> Dict:
        """Get job processing statistics."""
        total_jobs = len(self._jobs)
        
        status_counts = {}
        for job_data in self._jobs.values():
            status = job_data["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_jobs": total_jobs,
            "completed_results": len(self._results),
            "status_breakdown": status_counts,
            "memory_usage": {
                "jobs_stored": total_jobs,
                "results_stored": len(self._results),
                "max_jobs_limit": self._max_jobs
            }
        }


# Service instance
job_service = JobService()