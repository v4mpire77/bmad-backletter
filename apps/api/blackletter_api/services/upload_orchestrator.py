from __future__ import annotations

import asyncio
import logging
import uuid
from pathlib import Path
from typing import Awaitable, Callable, Optional, TypeVar

from fastapi import UploadFile

from ..models.job import Job
from .job_store import JobState, job_store
from .rulepack_loader import resolve_rulepack_version, load_rulepack
from .storage import save_upload
from .extractor import extract_text
from .detectors import run_detectors

logger = logging.getLogger(__name__)


async def submit_upload(file: UploadFile, rulepack_version: Optional[str] = None) -> Job:
    job_id = str(uuid.uuid4())
    pinned_version = resolve_rulepack_version(rulepack_version)

    job = await job_store.create_job(job_id=job_id, rulepack_version=pinned_version)

    # Persist the upload before returning; background task operates on path.
    path = await save_upload(file)
    content_type = file.content_type or "application/octet-stream"

    # Schedule background processing; avoid logging raw content/PII.
    asyncio.create_task(_process_job(job_id, path, content_type, pinned_version))

    return job


T = TypeVar("T")


async def with_retries(
    op_factory: Callable[[], Awaitable[T]], timeout_seconds: float, retries: int
) -> T:
    attempts = 0
    while True:
        try:
            return await asyncio.wait_for(op_factory(), timeout=timeout_seconds)
        except Exception as exc:  # noqa: BLE001
            attempts += 1
            if attempts > retries:
                raise exc
            await asyncio.sleep(0.05)


async def _process_job(job_id: str, file_path: Path, content_type: str, rulepack_version: str) -> None:
    try:
        await job_store.update_state(job_id, JobState.processing)

        # Step 1: file is already stored at file_path
        await asyncio.sleep(0)  # yield

        # Step 2: extract text (stub) with retry/timeout behavior.
        async def extract_text() -> str:
            return await extract_text(file_path, content_type)

        extracted_text = await with_retries(extract_text, timeout_seconds=2.0, retries=2)

        # Step 3: run detectors using pinned rulepack (stubbed) with retry/timeout.
        async def run_detectors_op() -> dict:
            rp = load_rulepack(version=rulepack_version)
            return run_detectors(extracted_text, rp.__dict__ if hasattr(rp, "__dict__") else rp)

        detector_results = await with_retries(run_detectors_op, timeout_seconds=5.0, retries=2)

        # Persist results
        await job_store.set_result(job_id, detector_results)
        await job_store.update_state(job_id, JobState.completed)
        logger.info("job %s completed with rulepack %s", job_id, rulepack_version)
    except Exception as exc:  # noqa: BLE001
        reason = f"processing failed: {exc.__class__.__name__}"
        await job_store.update_state(job_id, JobState.failed, error_reason=reason)
        logger.exception("job %s failed", job_id)
