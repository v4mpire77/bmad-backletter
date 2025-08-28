from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple
from uuid import UUID
from enum import Enum

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


class JobState(str, Enum):
    RECEIVED = "RECEIVED"
    EXTRACTED = "EXTRACTED"
    SEGMENTED = "SEGMENTED"
    GDPR_LEGAL_DONE = "GDPR_LEGAL_DONE"
    GC_DONE = "GC_DONE"
    REPORTED = "REPORTED"


class AnalysisSummary(BaseModel):
    id: str
    filename: str
    created_at: str
    size: int
    verdicts: VerdictCounts
    state: JobState
