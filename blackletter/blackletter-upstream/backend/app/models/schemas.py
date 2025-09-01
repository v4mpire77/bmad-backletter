"""
Blackletter GDPR Processor - Pydantic Schemas
Context Engineering Framework v2.0.0 Compliant
Follows build guide specifications for Issue, Coverage, and Job models
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum
import uuid


class JobStatusEnum(str, Enum):
    """Job processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SeverityEnum(str, Enum):
    """Issue severity levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class IssueTypeEnum(str, Enum):
    """Issue type classification."""
    GDPR = "GDPR"
    STATUTE = "Statute"
    CASE_LAW = "Case Law"


class IssueStatusEnum(str, Enum):
    """Issue resolution status."""
    OPEN = "Open"
    IN_REVIEW = "In Review"
    RESOLVED = "Resolved"


class CoverageStatusEnum(str, Enum):
    """GDPR Article coverage status."""
    OK = "OK"
    PARTIAL = "Partial"
    GAP = "GAP"


# Core schemas from build guide
class Issue(BaseModel):
    """
    Issue model following exact build guide specification.
    Represents a detected GDPR compliance issue.
    """
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True
    )
    
    id: str = Field(description="Unique issue identifier")
    doc_id: str = Field(description="Document identifier")
    clause_path: str = Field(description="Path to specific clause in document")
    type: IssueTypeEnum = Field(default=IssueTypeEnum.GDPR, description="Issue type classification")
    citation: str = Field(description="Legal citation (e.g., GDPR Article 28(3)(a))")
    severity: SeverityEnum = Field(description="Issue severity level")
    confidence: float = Field(ge=0, le=1, description="Confidence score for detection")
    status: IssueStatusEnum = Field(default=IssueStatusEnum.OPEN, description="Issue resolution status")
    snippet: str = Field(description="Relevant text snippet from document")
    recommendation: str = Field(description="Suggested remedy or improvement")
    created_at: str = Field(description="ISO timestamp of issue creation")


class Coverage(BaseModel):
    """
    GDPR Article coverage assessment.
    Tracks presence and quality of processor obligations.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    article: str = Field(description="GDPR Article reference (e.g., 28(3)(a))")
    status: CoverageStatusEnum = Field(description="Coverage assessment")
    confidence: float = Field(ge=0, le=1, description="Confidence in assessment")
    present: bool = Field(description="Whether obligation is present")
    strength: Literal["strong", "medium", "weak", "absent"] = Field(description="Quality of implementation")


# Job management schemas
class JobCreate(BaseModel):
    """Request schema for creating new analysis jobs."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    filename: str = Field(description="Uploaded file name")
    content_type: str = Field(description="File MIME type")
    file_size: int = Field(gt=0, description="File size in bytes")


class JobStatus(BaseModel):
    """Job status response schema."""
    model_config = ConfigDict(use_enum_values=True)
    
    job_id: str = Field(description="Unique job identifier")
    status: JobStatusEnum = Field(description="Current job status")
    progress: float = Field(ge=0, le=1, description="Processing progress (0.0 - 1.0)")
    created_at: datetime = Field(description="Job creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    message: Optional[str] = Field(default=None, description="Status message or error details")


class AnalysisResult(BaseModel):
    """Complete analysis results from GDPR processor."""
    model_config = ConfigDict(validate_assignment=True)
    
    issues: List[Issue] = Field(description="Detected compliance issues")
    coverage: List[Coverage] = Field(description="GDPR Article 28(3) coverage assessment")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Analysis metadata")


class JobResult(BaseModel):
    """Complete job result with analysis data."""
    model_config = ConfigDict(use_enum_values=True)
    
    job_id: str = Field(description="Job identifier")
    status: JobStatusEnum = Field(description="Final job status")
    analysis: Optional[AnalysisResult] = Field(default=None, description="Analysis results if successful")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    created_at: datetime = Field(description="Job creation timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Job completion timestamp")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")


# API response schemas
class JobCreateResponse(BaseModel):
    """Response schema for job creation (202 Accepted)."""
    job_id: str = Field(description="Created job identifier")
    status: JobStatusEnum = Field(default=JobStatusEnum.PENDING)
    message: str = Field(default="Job created successfully")
    location: str = Field(description="URL to check job status")


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    error: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    path: str = Field(description="Request path")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(description="Service health status")
    environment: str = Field(description="Current environment")
    framework_compliance: int = Field(description="Required compliance percentage")
    timestamp: float = Field(description="Response timestamp")


# File upload schemas
class FileUpload(BaseModel):
    """File upload metadata."""
    filename: str = Field(description="Original filename")
    content_type: str = Field(description="File MIME type")
    size: int = Field(gt=0, description="File size in bytes")
    checksum: Optional[str] = Field(default=None, description="File checksum for integrity")


# Utility functions for schema creation
def generate_job_id() -> str:
    """Generate unique job identifier."""
    return str(uuid.uuid4())


def generate_issue_id() -> str:
    """Generate unique issue identifier."""
    return f"issue_{uuid.uuid4().hex[:8]}"


def create_issue(
    doc_id: str,
    clause_path: str,
    citation: str,
    severity: SeverityEnum,
    confidence: float,
    snippet: str,
    recommendation: str,
    issue_type: IssueTypeEnum = IssueTypeEnum.GDPR
) -> Issue:
    """Create a new Issue instance with generated ID and timestamp."""
    return Issue(
        id=generate_issue_id(),
        doc_id=doc_id,
        clause_path=clause_path,
        type=issue_type,
        citation=citation,
        severity=severity,
        confidence=confidence,
        snippet=snippet,
        recommendation=recommendation,
        created_at=datetime.utcnow().isoformat()
    )


def create_coverage(
    article: str,
    status: CoverageStatusEnum,
    confidence: float,
    present: bool,
    strength: Literal["strong", "medium", "weak", "absent"]
) -> Coverage:
    """Create a new Coverage assessment."""
    return Coverage(
        article=article,
        status=status,
        confidence=confidence,
        present=present,
        strength=strength
    )