from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel


class Sentence(BaseModel):
    text: str
    page: int
    start: int
    end: int


class Document(BaseModel):
    id: str
    filename: str


class Job(BaseModel):
    id: str
    status: Literal["queued", "running", "done", "error"]
    analysis_id: Optional[str] = None
    error_reason: Optional[str] = None
    created_at: Optional[datetime] = None


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
