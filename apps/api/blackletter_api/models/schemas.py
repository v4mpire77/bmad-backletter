from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple
from enum import Enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ExtractionArtifact(BaseModel):
    analysis_id: UUID
    text_path: str
    page_map_path: str  # JSON or pickle path with {page: [start, end]}
    sentence_idx_path: str  # JSON or pickle path with [[start, end], ...]


class Detector(BaseModel):
    id: str
    anchors_any: Optional[List[str]] = None
    anchors_all: Optional[List[str]] = None
    redflags_any: Optional[List[str]] = None


class Rulepack(BaseModel):
    meta: Dict[str, object] = Field(default_factory=dict)
    detectors: List[Detector] = Field(default_factory=list)
    shared_lexicon: Dict[str, List[str]] = Field(default_factory=dict)


class DetectorSummary(BaseModel):
    id: str
    type: str
    description: Optional[str] = None
    lexicon: Optional[str] = None


class RulesSummary(BaseModel):
    name: str
    version: str
    detector_count: int
    detectors: List[DetectorSummary]
    lexicons: List[str]


class Finding(BaseModel):
    detector_id: str
    rule_id: str
    verdict: Literal["pass", "weak", "missing", "needs_review"]
    snippet: str
    page: int
    start: int
    end: int
    rationale: str
    reviewed: bool = False


class VerdictCounts(BaseModel):
    pass_count: int = 0
    weak_count: int = 0
    missing_count: int = 0
    needs_review_count: int = 0


class AnalysisSummary(BaseModel):
    id: str
    filename: str
    created_at: str
    size: int
    state: str
    verdicts: VerdictCounts


class JobState(str, Enum):
    queued = "queued"
    running = "running"
    done = "done"
    error = "error"


class JobStatus(BaseModel):
    id: str
    # Duplicate field for API compatibility with docs: expose job_id alongside id
    job_id: Optional[str] = None
    status: JobState
    analysis_id: Optional[str] = None
    # Story 1.2 response compatibility: alias JSON key to `error`
    error_reason: Optional[str] = Field(default=None, serialization_alias="error")
    created_at: Optional[datetime] = None


class ExportOptions(BaseModel):
    include_logo: bool = False
    include_meta: bool = True
    # Allow a few simple date formats for reports
    date_format: Literal["MDY", "DMY", "ISO"] = "ISO"


class ReportExport(BaseModel):
    id: str
    analysis_id: str
    filename: str
    created_at: str
    options: ExportOptions


class ExportOptions(BaseModel):
    include_logo: bool = True
    include_meta: bool = True
    date_format: Literal["YMD", "DMY", "MDY"] = "YMD"


class ReportExport(BaseModel):
    id: str
    analysis_id: str
    filename: str
    created_at: str
    options: ExportOptions
