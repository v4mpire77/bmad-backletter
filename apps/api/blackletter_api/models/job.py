from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class JobState(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Job(BaseModel):
    id: str
    state: JobState
    created_at: datetime
    updated_at: datetime
    error_reason: Optional[str] = None
    rulepack_version: str = Field(..., description="Pinned rulepack version used for this job")
    result: Optional[dict[str, Any]] = None


class JobCreateResponse(BaseModel):
    job_id: str

