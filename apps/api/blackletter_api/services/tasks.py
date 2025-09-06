from __future__ import annotations

import os
import time
import logging
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from redis import Redis

from ..models.schemas import JobState
from .celery_app import celery_app

logger = logging.getLogger(__name__)


@dataclass
class JobRecord:
    id: str
    status: JobState
    analysis_id: Optional[str]
    error_reason: Optional[str]
    created_at: datetime


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


async def create_contract_analysis_job(
    filename: str, 
    content_type: str, 
    file_content: bytes
) -> str:
    """
    Create a new contract analysis job with enhanced async processing.
    Integrated from v4mpire77/blackletter for improved job management.
    """
    try:
        # Generate unique job and analysis IDs
        job_id = str(uuid4())
        analysis_id = str(uuid4())
        
        # Create job record
        record = {
            "id": job_id,
            "status": JobState.queued.value,
            "analysis_id": analysis_id,
            "error_reason": "",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        redis_client.hset(_job_key(job_id), mapping=record)
        
        # Store file temporarily for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        # Queue the processing task
        process_contract_analysis.delay(job_id, analysis_id, tmp_file_path, filename)
        
        logger.info(f"Created analysis job {job_id} for file: {filename}")
        return job_id
        
    except Exception as e:
        logger.error(f"Error creating analysis job: {str(e)}", exc_info=True)
        raise


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_contract_analysis(self, job_id: str, analysis_id: str, file_path: str, filename: str):
    """
    Enhanced Celery task for contract analysis processing.
    Integrated from v4mpire77/blackletter for robust async processing with GDPR analysis.
    """
    try:
        # Update job status to running
        update_job_status(job_id, JobState.running)
        logger.info(f"Starting analysis for job {job_id}")
        
        # Step 1: Text extraction
        update_job_status(job_id, JobState.running, "Extracting text from document")
        extracted_text = extract_text_from_file(file_path, filename)
        
        # Step 2: GDPR analysis with enhanced analyzer
        update_job_status(job_id, JobState.running, "Running enhanced GDPR Article 28(3) analysis")
        findings, coverage = run_gdpr_analysis(extracted_text, analysis_id, filename)
        
        # Step 3: Store results
        update_job_status(job_id, JobState.running, "Storing analysis results")
        store_analysis_results(analysis_id, findings, coverage, filename)
        
        # Mark as complete
        update_job_status(job_id, JobState.done)
        logger.info(f"Enhanced GDPR analysis completed for job {job_id}: "
                   f"{len(findings)} findings, {coverage.present}/{coverage.total} obligations detected")
        
        # Clean up temp file
        try:
            os.unlink(file_path)
        except OSError:
            logger.warning(f"Could not clean up temp file: {file_path}")
            
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        update_job_status(job_id, JobState.error, error_msg)
        logger.error(f"Job {job_id} failed: {error_msg}", exc_info=True)
        raise self.retry(countdown=60, max_retries=3)


def extract_text_from_file(file_path: str, filename: str) -> str:
    """Extract text from uploaded file."""
    try:
        if filename.lower().endswith('.pdf'):
            # Simple PDF text extraction (placeholder)
            # In production, use PyMuPDF or similar
            with open(file_path, 'rb') as f:
                content = f.read()
                return f"Extracted text from PDF: {filename} (placeholder implementation)"
        
        elif filename.lower().endswith(('.docx', '.doc')):
            # Simple DOCX text extraction (placeholder)
            # In production, use python-docx or similar
            with open(file_path, 'rb') as f:
                content = f.read()
                return f"Extracted text from Word document: {filename} (placeholder implementation)"
        
        else:
            # Try to read as plain text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
    except Exception as e:
        logger.error(f"Error extracting text from {filename}: {str(e)}")
        raise


def run_gdpr_analysis(text: str, analysis_id: str, filename: str):
    """Run enhanced GDPR analysis using the integrated analyzer."""
    from .gdpr_analyzer import gdpr_analyzer
    return gdpr_analyzer.analyze_document(text, analysis_id, filename)


def store_analysis_results(analysis_id: str, findings, coverage, filename: str):
    """Store analysis results (placeholder implementation)."""
    # In production, this would store to database or filesystem
    logger.info(f"Stored analysis results for {analysis_id}: "
               f"{len(findings)} findings, coverage: {coverage.percentage:.1f}%")


def update_job_status(job_id: str, status: JobState, message: str = "") -> None:
    """Update job status in Redis."""
    key = _job_key(job_id)
    redis_client.hset(key, "status", status.value)
    if message:
        redis_client.hset(key, "error_reason", message)
    redis_client.hset(key, "updated_at", datetime.now(timezone.utc).isoformat())


def new_job(analysis_id: str | None = None) -> str:
    job_id = str(uuid4())
    record = {
        "id": job_id,
        "status": JobState.queued.value,
        "analysis_id": analysis_id or "",
        "error_reason": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    redis_client.hset(_job_key(job_id), mapping=record)
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info("New job created and queued", extra=log_extras)
    return job_id


def enqueue_job(
    job_id: str,
    analysis_id: str,
    filename: str,
    size: int,
    backend: str | None = None,
) -> None:
    """Enqueue the document processing job.

    Parameters
    ----------
    job_id, analysis_id, filename, size:
        Identifiers and metadata for the job to enqueue.
    backend:
        Execution backend. ``"sync"`` processes the job immediately within the
        current process, while ``"celery"`` dispatches the job to a Celery
        worker.  If ``None`` the backend defaults to ``"celery"``.

    Notes
    -----
    The previous implementation relied on the ``JOB_SYNC`` environment
    variable.  Explicitly passing the backend makes behaviour clearer and
    simplifies testing.
    """

    chosen = backend or "celery"
    if chosen == "sync":
        process_job(job_id, analysis_id, filename, size)
    elif chosen == "celery":
        process_job.delay(job_id, analysis_id, filename, size)
    else:
        raise ValueError(f"Unknown backend '{chosen}'")


def get_job(job_id: str) -> Optional[JobRecord]:
    data = redis_client.hgetall(_job_key(job_id))
    if not data:
        return None
    return JobRecord(
        id=data["id"],
        status=JobState(data["status"]),
        analysis_id=data.get("analysis_id") or None,
        error_reason=data.get("error_reason") or None,
        created_at=datetime.fromisoformat(data["created_at"]),
    )


def set_status(job_id: str, status: JobState, error_reason: str | None = None) -> None:
    if not redis_client.exists(_job_key(job_id)):
        return
    redis_client.hset(
        _job_key(job_id),
        mapping={"status": status.value, "error_reason": error_reason or ""},
    )


@celery_app.task(name="process_job")
def process_job(job_id: str, analysis_id: str, filename: str, size: int) -> None:
    """Orchestration work for the document processing job."""
    log_extras = {"job_id": job_id, "analysis_id": analysis_id}
    logger.info("Starting job processing", extra=log_extras)

    try:
        set_status(job_id, JobState.running)
        a_dir = analysis_dir(analysis_id)
        source_path = a_dir / filename

        write_analysis_json(analysis_id, filename=filename, size=size)

        # Stage 1: Extraction
        t_start_ext = time.time()
        try:
            extraction_path = run_extraction(analysis_id, source_path, a_dir)
            record_extraction_artifact(
                analysis_id=analysis_id,
                job_id=job_id,
                artifact_path=str(extraction_path),
            )
            t_end_ext = time.time()
            latency_ms = round((t_end_ext - t_start_ext) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.info("Extraction completed successfully", extra=log_extras)

        except Exception as e:
            t_end_ext = time.time()
            latency_ms = round((t_end_ext - t_start_ext) * 1000)
            log_extras["latency_ms"] = latency_ms
            logger.error("Extraction failed", extra=log_extras)
            set_status(job_id, JobState.error, error_reason=f"extraction_failed: {e}")
            return

        # Stage 2: Detection (optional if detectors unavailable)
        try:
            from .detector_runner import run_detectors  # Lazy import to avoid hard dependency during tests
        except Exception:
            run_detectors = None  # type: ignore

        if run_detectors is not None:
            t_start_det = time.time()
            try:
                findings = run_detectors(analysis_id, str(extraction_path))
                for f in findings:
                    window = build_window(analysis_id, f.start, f.end)
                    record_evidence_artifact(
                        analysis_id=analysis_id,
                        job_id=job_id,
                        window=window,
                    )
                generate_html_export(analysis_id, findings)
                t_end_det = time.time()
                latency_ms = round((t_end_det - t_start_det) * 1000)
                log_extras["latency_ms"] = latency_ms
                logger.info("Detection completed successfully", extra=log_extras)
            except Exception as e:
                t_end_det = time.time()
                latency_ms = round((t_end_det - t_start_det) * 1000)
                log_extras["latency_ms"] = latency_ms
                logger.error("Detection failed", extra=log_extras)
                set_status(job_id, JobState.error, error_reason=f"detection_failed: {e}")
                return
        else:
            logger.info("Detection skipped: detectors unavailable", extra=log_extras)

        set_status(job_id, JobState.done)
        logger.info("Job processing completed successfully", extra=log_extras)

    except Exception as e:
        logger.error("Unhandled error in job processing", extra=log_extras)
        set_status(job_id, JobState.error, error_reason=str(e))
