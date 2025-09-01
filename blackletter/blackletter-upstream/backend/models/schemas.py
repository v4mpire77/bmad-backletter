import uuid
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ReviewResult(BaseModel):
    summary: str
    risks: List[str]


class Issue(BaseModel):
    id: str
    docId: str
    docName: str
    clausePath: str
    type: Literal["GDPR", "Statute", "Case Law"]
    citation: str
    severity: Literal["High", "Medium", "Low"]
    confidence: float
    status: Literal["Open", "In Review", "Resolved"]
    owner: Optional[str] = None
    snippet: str
    recommendation: str
    createdAt: str


class ContractType(str, Enum):
    VENDOR_DPA = "vendor_dpa"
    MSA = "msa"
    PRIVACY_POLICY = "privacy_policy"
    PROCESSING_AGREEMENT = "processing_agreement"


class Jurisdiction(str, Enum):
    EU = "EU"
    UK = "UK"
    US_CA = "US_CA"  # California, USA
    US_CO = "US_CO"  # Colorado, USA


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobCreationResponse(BaseModel):
    job_id: uuid.UUID = Field(
        ..., description="The unique identifier for the created job."
    )
    status: JobStatus = Field(
        JobStatus.QUEUED, description="The initial status of the job."
    )
    created_at: datetime = Field(..., description="When the job was created.")


class JobStatusResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    error_message: Optional[str] = Field(
        None, description="Details of the error if the job failed."
    )
    progress: Optional[str] = Field(None, description="Current processing step.")

    class Config:
        from_attributes = True


class AnalysisIssue(BaseModel):
    rule_id: str
    description: str
    compliant: bool
    severity: str  # "high", "medium", "low"
    details: str
    citation: Optional[str] = None
    recommendation: Optional[str] = None


class AnalysisResult(BaseModel):
    summary: str = Field(
        ..., description="A high-level summary of the compliance check."
    )
    overall_score: float = Field(..., description="Overall compliance score (0-100).")
    clauses_found: int
    issues_detected: int
    issues: List[AnalysisIssue]
    processing_time_seconds: Optional[float] = None


class JobResultResponse(JobStatusResponse):
    result: Optional[AnalysisResult] = Field(
        None,
        description="The detailed analysis result, available when status is 'completed'.",
    )
    report_url: Optional[str] = Field(
        None, description="URL to download the PDF report."
    )

    class Config:
        from_attributes = True
