from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, root_validator, validator


class AnalysisStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    archived = "archived"


class AnalysisSort(str, Enum):
    created_at = "created_at"
    created_at_desc = "-created_at"
    findings = "findings"
    findings_desc = "-findings"


class AnalysisBase(BaseModel):
    """
    Canonical representation of an analysis for the dashboard.

    Fields here define the data contract for list/detail views and will be
    used by services and API routers. Validators ensure safe defaults and
    consistent values so that later integration is straightforward.
    """

    id: str = Field(..., description="Opaque ID (UUID or ULID)")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: Optional[datetime] = Field(
        None, description="Last update timestamp (UTC)"
    )
    filename: str = Field(..., description="Original uploaded filename")
    filesize: int = Field(..., ge=0, description="Size in bytes, non-negative")
    status: AnalysisStatus = Field(
        AnalysisStatus.pending, description="Processing lifecycle state"
    )
    rulepack_version: Optional[str] = Field(
        None, description="Pinned rulepack version used for analysis"
    )
    findings_count: int = Field(0, ge=0, description="Number of findings")
    uploader: Optional[str] = Field(None, description="Username or user ID")
    tags: List[str] = Field(default_factory=list, description="Freeform labels")
    archived: bool = Field(False, description="Hidden from primary views")

    class Config:
        orm_mode = True  # allow population from ORM objects later

    @validator("filename")
    def filename_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("filename must be a non-empty string")
        return v.strip()

    @validator("tags", each_item=True)
    def normalize_tags(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("tags cannot contain empty strings")
        return nv


class AnalysisListItem(AnalysisBase):
    """Slimmed item for list/table views."""

    # identical to base for now; can be narrowed later if needed
    pass


class AnalysisDetail(AnalysisBase):
    """Extended detail view model if needed later."""

    # placeholder for future detail-only fields (e.g., summary, durations)
    pass


class AnalysisListFilters(BaseModel):
    """
    Query model for server-side filtering & pagination.
    Encodes dashboard filter bar + search + sorting.
    """

    q: Optional[str] = Field(None, description="Free-text search (filename, tags, user)")
    status: Optional[List[AnalysisStatus]] = Field(
        None, description="Filter by one or more statuses"
    )
    date_from: Optional[datetime] = Field(None, description="Created at >= this UTC time")
    date_to: Optional[datetime] = Field(None, description="Created at < this UTC time")
    rulepack: Optional[str] = Field(None, description="Rulepack version filter")
    uploader: Optional[str] = Field(None, description="Filter by uploader")
    min_findings: Optional[int] = Field(None, ge=0)
    max_findings: Optional[int] = Field(None, ge=0)
    sort: AnalysisSort = Field(AnalysisSort.created_at_desc)
    limit: int = Field(25, ge=1, le=100)
    cursor: Optional[str] = Field(
        None, description="Opaque server-provided cursor for pagination"
    )

    @root_validator
    def check_ranges(cls, values):
        df, dt = values.get("date_from"), values.get("date_to")
        if df and dt and df >= dt:
            raise ValueError("date_from must be earlier than date_to")
        mn, mx = values.get("min_findings"), values.get("max_findings")
        if mn is not None and mx is not None and mn > mx:
            raise ValueError("min_findings cannot be greater than max_findings")
        return values


class AnalysisListResponse(BaseModel):
    items: List[AnalysisListItem]
    next_cursor: Optional[str] = None
    total_estimate: Optional[int] = Field(
        None, description="Optional approximate count for UX hints"
    )

