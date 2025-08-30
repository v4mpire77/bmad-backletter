from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Awaitable, Callable, Optional, TypeVar

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


async def _process_job(job_id: str, filename: str, rulepack_version: str) -> None:
    try:
        await job_store.update_state(job_id, JobState.processing)

        # Step 1: store file (stub) - pretend we stored securely.
        await asyncio.sleep(0.01)

        # Step 2: extract text (stub) with retry/timeout behavior.
        async def extract_text() -> str:
            await asyncio.sleep(0.01)
            return ""  # intentionally omit raw content

        extracted_text = await with_retries(extract_text, timeout_seconds=2.0, retries=2)

        # Step 3: run detectors using pinned rulepack (stubbed) with retry/timeout.
        async def run_detectors() -> dict:
            await asyncio.sleep(0.01)
            return {"rulepack": rulepack_version, "findings": []}

        detector_results = await with_retries(run_detectors, timeout_seconds=5.0, retries=2)

        # Persist results
        await job_store.set_result(job_id, detector_results)
        await job_store.update_state(job_id, JobState.completed)
        logger.info("job %s completed with rulepack %s", job_id, rulepack_version)
    except Exception as exc:  # noqa: BLE001
        reason = f"processing failed: {exc.__class__.__name__}"
        await job_store.update_state(job_id, JobState.failed, error_reason=reason)
        logger.exception("job %s failed", job_id)
