from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Optional

from fastapi import UploadFile

from ..models.job import Job
from .job_store import JobState, job_store
from .rulepack_loader import resolve_rulepack_version

logger = logging.getLogger(__name__)


async def submit_upload(file: UploadFile, rulepack_version: Optional[str] = None) -> Job:
    job_id = str(uuid.uuid4())
    pinned_version = resolve_rulepack_version(rulepack_version)

    job = await job_store.create_job(job_id=job_id, rulepack_version=pinned_version)

    # Schedule background processing; avoid logging raw content/PII.
    asyncio.create_task(_process_job(job_id, file.filename, pinned_version))

    return job


async def _process_job(job_id: str, filename: str, rulepack_version: str) -> None:
    try:
        await job_store.update_state(job_id, JobState.processing)

        # Step 1: store file (stub) - pretend we stored securely.
        await asyncio.sleep(0.01)

        # Step 2: extract text (stub) with retry/timeout placeholders.
        await asyncio.sleep(0.01)
        extracted_text = ""  # intentionally omit raw content

        # Step 3: run detectors using pinned rulepack (stubbed)
        await asyncio.sleep(0.01)
        detector_results = {
            "rulepack": rulepack_version,
            "findings": [],
        }

        # Persist results
        await job_store.set_result(job_id, detector_results)
        await job_store.update_state(job_id, JobState.completed)
        logger.info("job %s completed with rulepack %s", job_id, rulepack_version)
    except Exception as exc:  # noqa: BLE001
        reason = f"processing failed: {exc.__class__.__name__}"
        await job_store.update_state(job_id, JobState.failed, error_reason=reason)
        logger.exception("job %s failed", job_id)

