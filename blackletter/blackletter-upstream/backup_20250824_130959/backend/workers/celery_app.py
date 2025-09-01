<<<<<<< HEAD
"""
Blackletter GDPR Processor - Celery Configuration
Context Engineering Framework v2.0.0 Compliant
Background job processing with Redis message broker
"""
import os
import logging
from celery import Celery
from celery.signals import worker_ready, worker_shutdown
from kombu import Queue

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery(
    "blackletter_gdpr_processor",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["workers.celery_app"]
)

# Celery configuration
celery_app.conf.update(
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task routing
    task_routes={
        "workers.celery_app.analyze_contract_task": {"queue": "gdpr_analysis"},
        "workers.celery_app.cleanup_task": {"queue": "maintenance"}
    },
    
    # Queue configuration
    task_default_queue="default",
    task_queues=(
        Queue("default"),
        Queue("gdpr_analysis"),
        Queue("maintenance")
    ),
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # Task time limits
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,       # 10 minutes hard limit
    
    # Result backend settings
    result_expires=3600,       # 1 hour
    result_persistent=True,
    
    # Error handling
    task_reject_on_worker_lost=True,
    task_ignore_result=False,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Worker event handlers
@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    """Handle worker ready event."""
    logger.info(f"Celery worker ready: {sender}")
    logger.info("Context Engineering Framework v2.0.0 - GDPR Analysis Worker")

@worker_shutdown.connect
def worker_shutdown_handler(sender=None, **kwargs):
    """Handle worker shutdown event."""
    logger.info(f"Celery worker shutting down: {sender}")


# Import task definitions
@celery_app.task(bind=True, name="workers.celery_app.analyze_contract_task")
def analyze_contract_task(self, job_id: str, file_path: str, filename: str):
    """
    Analyze contract for GDPR Article 28(3) compliance.
    
    Args:
        job_id: Unique job identifier
        file_path: Path to uploaded contract file
        filename: Original filename
    """
    import asyncio
    import time
    from datetime import datetime
    
    try:
        logger.info(f"Starting GDPR analysis for job {job_id}: {filename}")
        
        # Update job status
        from app.services.job_service import job_service
        asyncio.run(job_service.update_job_status(
            job_id, 
            from app.models.schemas import JobStatusEnum
            JobStatusEnum.PROCESSING,
            progress=0.2,
            message="Reading contract file"
        ))
        
        # Extract text from file
        contract_text = extract_text_from_file(file_path, filename)
        
        # Update progress
        asyncio.run(job_service.update_job_status(
            job_id,
            JobStatusEnum.PROCESSING,
            progress=0.4,
            message="Analyzing GDPR compliance"
        ))
        
        # Perform GDPR analysis
        from app.services.gdpr_analyzer import gdpr_analyzer
        from app.models.schemas import AnalysisResult
        
        issues, coverage = gdpr_analyzer.analyze_processor_obligations(
            contract_text, 
            doc_id=job_id
        )
        
        # Update progress
        asyncio.run(job_service.update_job_status(
            job_id,
            JobStatusEnum.PROCESSING,
            progress=0.8,
            message="Finalizing results"
        ))
        
        # Create analysis result
        analysis_result = AnalysisResult(
            issues=issues,
            coverage=coverage,
            metadata={
                "filename": filename,
                "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "issues_found": len(issues),
                "coverage_articles": len(coverage),
                "processing_node": self.request.hostname,
                "task_id": self.request.id
            }
        )
        
        # Complete job
        asyncio.run(job_service.complete_job(
            job_id,
            analysis_result=analysis_result
        ))
        
        logger.info(f"Completed GDPR analysis for job {job_id}: {len(issues)} issues found")
        
        return {
            "job_id": job_id,
            "status": "completed",
            "issues_count": len(issues),
            "coverage_count": len(coverage)
        }
        
    except Exception as e:
        logger.error(f"Error analyzing contract for job {job_id}: {str(e)}", exc_info=True)
        
        # Mark job as failed
        try:
            asyncio.run(job_service.complete_job(
                job_id,
                analysis_result=None,
                error=f"Analysis failed: {str(e)}"
            ))
        except Exception as cleanup_error:
            logger.error(f"Failed to update job status after error: {cleanup_error}")
        
        # Re-raise for Celery error handling
        raise


def extract_text_from_file(file_path: str, filename: str) -> str:
    """
    Extract text content from uploaded file.
    
    Args:
        file_path: Path to file
        filename: Original filename for type detection
        
    Returns:
        Extracted text content
    """
    try:
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'txt':
            # Plain text file
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        elif file_extension == 'pdf':
            # PDF file - requires pypdf or similar
            try:
                import pypdf
                with open(file_path, 'rb') as f:
                    reader = pypdf.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                logger.warning("pypdf not available, treating PDF as text")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
                    
        elif file_extension in ['doc', 'docx']:
            # Word document - requires python-docx
            try:
                import docx
                doc = docx.Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                logger.warning("python-docx not available, treating as text")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        else:
            # Default to text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
    except Exception as e:
        logger.error(f"Error extracting text from {filename}: {str(e)}")
        raise ValueError(f"Failed to extract text from file: {str(e)}")


@celery_app.task(name="workers.celery_app.cleanup_task")
def cleanup_task():
    """
    Periodic cleanup task for maintenance.
    Removes old job data and temporary files.
    """
    try:
        logger.info("Starting periodic cleanup task")
        
        # Cleanup job service (if accessible)
        import asyncio
        from app.services.job_service import job_service
        
        asyncio.run(job_service._cleanup_old_jobs())
        
        # Cleanup temporary files
        import tempfile
        import glob
        
        temp_dir = tempfile.gettempdir()
        old_files = glob.glob(os.path.join(temp_dir, "tmp*"))
        
        cleaned_count = 0
        for temp_file in old_files:
            try:
                # Remove files older than 1 hour
                if os.path.getmtime(temp_file) < time.time() - 3600:
                    os.remove(temp_file)
                    cleaned_count += 1
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {temp_file}: {e}")
        
        logger.info(f"Cleanup completed: removed {cleaned_count} temporary files")
        
        return {"cleaned_files": cleaned_count}
        
    except Exception as e:
        logger.error(f"Cleanup task failed: {str(e)}", exc_info=True)
        raise


# Periodic task schedule
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "cleanup-every-hour": {
        "task": "workers.celery_app.cleanup_task",
        "schedule": crontab(minute=0),  # Every hour at minute 0
    },
}
celery_app.conf.timezone = "UTC"


if __name__ == "__main__":
    # For direct execution
    celery_app.start()
=======
from celery import Celery

from ..core.config import settings

celery_app = Celery(
    "blackletter_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["backend.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=86400,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_pool_limit=10,
    task_routes={
        "backend.workers.tasks.process_contract": {"queue": "contract_processing"}
    },
)
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
