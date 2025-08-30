from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, Optional, Tuple

from ..models.job import Job, JobState


class InMemoryJobStore:
    def __init__(self) -> None:
        self._jobs: Dict[str, Job] = {}
        self._lock = asyncio.Lock()

    async def create_job(self, job_id: str, rulepack_version: str) -> Job:
        async with self._lock:
            now = datetime.utcnow()
            job = Job(
                id=job_id,
                state=JobState.queued,
                created_at=now,
                updated_at=now,
                rulepack_version=rulepack_version,
            )
            self._jobs[job_id] = job
            return job

    async def get_job(self, job_id: str) -> Optional[Job]:
        async with self._lock:
            return self._jobs.get(job_id)

    async def update_state(
        self, job_id: str, state: JobState, error_reason: Optional[str] = None
    ) -> Optional[Job]:
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job.state = state
            job.updated_at = datetime.utcnow()
            job.error_reason = error_reason
            self._jobs[job_id] = job
            return job

    async def set_result(self, job_id: str, result: dict) -> Optional[Job]:
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job.result = result
            job.updated_at = datetime.utcnow()
            self._jobs[job_id] = job
            return job

    async def stats(self) -> dict:
        async with self._lock:
            counts = {s.value: 0 for s in JobState}
            total = 0
            durations: list[float] = []
            for job in self._jobs.values():
                counts[job.state.value] = counts.get(job.state.value, 0) + 1
                total += 1
                if job.state == JobState.completed:
                    durations.append((job.updated_at - job.created_at).total_seconds())
            avg = sum(durations) / len(durations) if durations else None
            return {
                "counts": counts,
                "total_jobs": total,
                "average_processing_seconds": avg,
            }


# Singleton-ish store for app lifetime
job_store = InMemoryJobStore()
