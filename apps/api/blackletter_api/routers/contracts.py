from __future__ import annotations

import os
from uuid import uuid4

from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.entities import Analysis
from ..models.schemas import (
    ContractValidationStatus,
    JobStatus,
    JobState,
    ValidationResults,
)
from ..services import storage
from ..services.tasks import new_job, process_job


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
    db: Session = Depends(get_db),
) -> JobStatus:
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
        raise HTTPException(status_code=415, detail="unsupported_file_type")

    # Create the analysis record in the database
    analysis = Analysis(
        filename=file.filename or "untitled",
        size_bytes=0,  # We don't know the size until after saving
        mime_type=file.content_type or "application/octet-stream",
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    analysis_id = str(analysis.id)

    target_dir = storage.analysis_dir(analysis_id)
    safe_name = storage.sanitize_filename(file.filename or f"upload{ext}")
    # Ensure extension matches allowed type inferred
    if not safe_name.lower().endswith(ext):
        safe_name = f"{safe_name}{ext}"
    target_path = target_dir / safe_name

    try:
        size = storage.save_upload(file, target_path, max_bytes=MAX_BYTES)
        analysis.size_bytes = size
        db.commit()
    except ValueError as e:
        if str(e) == "file_too_large":
            raise HTTPException(status_code=413, detail="file_too_large")
        raise
    except OSError as e:
        raise HTTPException(status_code=500, detail="disk_io_error") from e

    job_id = new_job(analysis_id=analysis_id)

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


@router.get(
    "/contracts/validation-status/{job_id}",
    response_model=ContractValidationStatus,
)
async def get_contract_validation_status(job_id: str) -> ContractValidationStatus:
    """
    Test endpoint for CWC demonstration - returns contract validation status
    This endpoint would be perfect for testing CWC integration
    """
    return ContractValidationStatus(
        job_id=job_id,
        status="completed",
        validation_results=ValidationResults(
            gdpr_compliance="pass",
            article_28_checks="pass",
            data_processing_agreement="pass",
            security_measures="pass",
        ),
        recommendations=[
            "Contract meets GDPR Article 28 requirements",
            "All processor obligations are properly addressed",
            "Security measures are adequate",
        ],
        timestamp=datetime.fromisoformat("2024-01-15T10:30:00+00:00"),
    )

