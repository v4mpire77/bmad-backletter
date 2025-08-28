from __future__ import annotations

import os
import time
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from ..models.schemas import JobStatus, JobState
from ..services import storage
from ..services.tasks import new_job, process_job

logger = logging.getLogger(__name__)
router = APIRouter(tags=["contracts"])


ALLOWED_MIME = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}
MAX_BYTES = 10 * 1024 * 1024


@router.post("/contracts", status_code=201, response_model=JobStatus)
async def upload_contract(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
) -> JobStatus:
    upload_start = time.time()
    
    # Validate type/extension
    ext = None
    if file.content_type in ALLOWED_MIME:
        ext = ALLOWED_MIME[file.content_type]
    else:
        # Fallback: infer from filename
        lower = (file.filename or "").lower()
        if lower.endswith(".pdf"):
            ext = ".pdf"
        elif lower.endswith(".docx"):
            ext = ".docx"
    if ext is None:
        logger.warning("Unsupported file type attempted", extra={
            "filename": file.filename,
            "content_type": file.content_type
        })
        raise HTTPException(status_code=415, detail="unsupported_file_type")

    analysis_id = str(uuid4())
    target_dir = storage.analysis_dir(analysis_id)
    safe_name = storage.sanitize_filename(file.filename or f"upload{ext}")
    # Ensure extension matches allowed type inferred
    if not safe_name.lower().endswith(ext):
        safe_name = f"{safe_name}{ext}"
    target_path = target_dir / safe_name

    try:
        size = storage.save_upload(file, target_path, max_bytes=MAX_BYTES)
    except ValueError as e:
        if str(e) == "file_too_large":
            logger.warning("File too large rejected", extra={
                "filename": file.filename,
                "size_bytes": getattr(file, 'size', 'unknown'),
                "max_bytes": MAX_BYTES
            })
            raise HTTPException(status_code=413, detail="file_too_large")
        raise
    except OSError as e:
        logger.error("Disk I/O error during upload", extra={
            "filename": file.filename,
            "error": str(e)
        })
        raise HTTPException(status_code=500, detail="disk_io_error") from e

    job_id = new_job(analysis_id=analysis_id)
    
    # Log successful upload
    upload_time = round((time.time() - upload_start) * 1000)
    logger.info("Contract upload successful", extra={
        "job_id": job_id,
        "analysis_id": analysis_id,
        "filename": safe_name,
        "size_bytes": size,
        "upload_latency_ms": upload_time
    })

    # Run processing either sync (tests/dev) or via background task
    if os.getenv("JOB_SYNC", "0") == "1":
        process_job(job_id, analysis_id=analysis_id, filename=safe_name, size=size)
    else:
        background_tasks.add_task(
            process_job, job_id, analysis_id, safe_name, size
        )

    return JobStatus(
        id=job_id,
        job_id=job_id,
        status=JobState.queued,
        analysis_id=analysis_id,
    )


@router.get("/contracts/validation-status/{job_id}")
async def get_contract_validation_status(job_id: str):
    """
    Test endpoint for CWC demonstration - returns contract validation status
    This endpoint would be perfect for testing CWC integration
    """
    return {
        "job_id": job_id,
        "status": "completed",
        "validation_results": {
            "gdpr_compliance": "pass",
            "article_28_checks": "pass",
            "data_processing_agreement": "pass",
            "security_measures": "pass"
        },
        "recommendations": [
            "Contract meets GDPR Article 28 requirements",
            "All processor obligations are properly addressed",
            "Security measures are adequate"
        ],
        "timestamp": "2024-01-15T10:30:00Z"
    }

