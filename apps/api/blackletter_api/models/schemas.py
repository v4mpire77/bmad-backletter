from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple
from enum import Enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error envelope for API responses."""

    code: str
    message: str


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
    category: Optional[str] = None
    confidence: Optional[float] = None
    reviewed: bool = False
    weak_language_detected: bool = False
    lexicon_version: Optional[str] = None


class VerdictCounts(BaseModel):
    pass_count: int = 0
    weak_count: int = 0
    missing_count: int = 0
    needs_review_count: int = 0


class Coverage(BaseModel):
    """Story 4.2 - Coverage model for detector coverage visualization."""
    present: int = 0
    total: int = 8  # Expected 8 detectors for Art 28 (a-h)
    percentage: float = 0.0
    missing_detectors: List[str] = Field(default_factory=list)
    status: Literal["complete", "incomplete", "unknown"] = "unknown"


class AnalysisSummary(BaseModel):
    id: str
    filename: str
    created_at: str
    size: int
    state: str
    verdicts: VerdictCounts
    coverage: Optional[Coverage] = None  # Story 4.2 - Coverage information


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


class JobCreateResponse(BaseModel):
    """Enhanced response schema for job creation with 202 Accepted pattern.
    Integrated from v4mpire77/blackletter for async job processing.
    """
    job_id: str = Field(description="Created job identifier")
    status: JobState = Field(default=JobState.queued, description="Initial job status")
    message: str = Field(default="Job created successfully", description="Status message")
    location: str = Field(description="URL to check job status")
    analysis_id: Optional[str] = Field(default=None, description="Analysis ID if available")


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


class ValidationResults(BaseModel):
    gdpr_compliance: str
    article_28_checks: str
    data_processing_agreement: str
    security_measures: str


class ContractValidationStatus(BaseModel):
    job_id: str
    status: str
    validation_results: ValidationResults
    recommendations: List[str]
    timestamp: datetime


class QASource(BaseModel):
    """Source citation for a Q&A response."""
    page: int
    content: str


class QAResponse(BaseModel):
    """Answer returned from the document Q&A endpoint."""
    answer: str
    sources: List[QASource] = Field(default_factory=list)
