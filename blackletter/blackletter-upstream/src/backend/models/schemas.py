from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

Severity = Literal["High", "Medium", "Low"]
IssueType = Literal["GDPR", "Statute", "Case Law"]
IssueStatus = Literal["Open", "In Review", "Resolved"]

class Issue(BaseModel):
    id: str
    docId: str
    docName: str
    clausePath: str
    type: IssueType
    citation: str
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    status: IssueStatus = "Open"
    owner: Optional[str] = None
    snippet: str
    recommendation: str
    createdAt: str

class ReviewResult(BaseModel):
    summary: str
    risks: List[str] = []
    redlines: Dict[str, Any] = {}
    next_actions: List[str] = []
    issues: List[Issue] = []
