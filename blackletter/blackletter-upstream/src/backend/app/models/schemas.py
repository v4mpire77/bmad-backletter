"""
Pydantic schemas for Blackletter Systems.

This module defines the data models used throughout the application.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

# Common enums
class DocumentType(str, Enum):
    """Types of documents that can be processed"""
    CONTRACT = "contract"
    LEGISLATION = "legislation"
    CASE = "case"
    ARTICLE = "article"
    OTHER = "other"

class IssueSeverity(str, Enum):
    """Severity levels for issues"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Request models
class DocumentUploadRequest(BaseModel):
    """Request model for document upload"""
    document_type: DocumentType = Field(default=DocumentType.CONTRACT)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

class ContractReviewRequest(BaseModel):
    """Request model for contract review"""
    document_key: str = Field(..., description="S3 key of the uploaded document")
    document_type: DocumentType = Field(default=DocumentType.CONTRACT)
    playbook: Optional[str] = Field(default=None, description="Name of the playbook to use")
    metadata: Optional[Dict[str, Any]] = Field(default=None)

class ResearchQueryRequest(BaseModel):
    """Request model for research query"""
    query: str = Field(..., description="Research query")
    filters: Optional[Dict[str, Any]] = Field(default=None)
    limit: int = Field(default=10, ge=1, le=100)

class ComplianceIngestRequest(BaseModel):
    """Request model for compliance feed ingest"""
    url: HttpUrl = Field(..., description="URL of the feed to ingest")
    source_type: str = Field(..., description="Type of source (e.g., ICO, FCA)")
    metadata: Optional[Dict[str, Any]] = Field(default=None)

# Response models
class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""
    document_key: str = Field(..., description="S3 key of the uploaded document")
    document_type: DocumentType
    upload_time: datetime
    metadata: Optional[Dict[str, Any]] = None

class Issue(BaseModel):
    """Model for document issues"""
    text: str = Field(..., description="Text of the issue")
    start: int = Field(..., description="Start position in document")
    end: int = Field(..., description="End position in document")
    severity: IssueSeverity = Field(default=IssueSeverity.MEDIUM)
    comment: Optional[str] = None
    suggestion: Optional[str] = None

class Citation(BaseModel):
    """Model for legal citations"""
    text: str = Field(..., description="Original citation text")
    case_id: str = Field(..., description="Case identifier")
    para: Optional[int] = Field(default=None, description="Paragraph number")
    year: Optional[str] = None
    court: Optional[str] = None
    number: Optional[str] = None
    source_type: str = Field(default="case")
    source_id: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    valid: bool = Field(default=True)

class ContractReviewResponse(BaseModel):
    """Response model for contract review"""
    document_key: str
    summary_key: str = Field(..., description="S3 key of the summary markdown")
    review_key: str = Field(..., description="S3 key of the review JSON")
    redlined_key: Optional[str] = Field(default=None, description="S3 key of the redlined document")
    issues_count: Dict[str, int] = Field(..., description="Count of issues by severity")
    processing_time: float = Field(..., description="Processing time in seconds")

class ResearchResult(BaseModel):
    """Model for research results"""
    text: str = Field(..., description="Result text")
    source: str = Field(..., description="Source document")
    score: float = Field(..., description="Relevance score")
    page: Optional[int] = None
    paragraph: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class ResearchQueryResponse(BaseModel):
    """Response model for research query"""
    query: str
    answer: str = Field(..., description="Generated answer")
    citations: List[Citation] = Field(default_factory=list)
    results: List[ResearchResult] = Field(default_factory=list)
    processing_time: float

class ComplianceItem(BaseModel):
    """Model for compliance items"""
    title: str
    summary: str
    source: str
    url: HttpUrl
    date: datetime
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

class ComplianceIngestResponse(BaseModel):
    """Response model for compliance feed ingest"""
    source_type: str
    items_count: int
    items: List[ComplianceItem] = Field(default_factory=list)
    processing_time: float

# Event models
class WebhookEvent(BaseModel):
    """Model for webhook events"""
    event_type: str = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any] = Field(..., description="Event data")

# Database models
class DocumentRecord(BaseModel):
    """Model for document database records"""
    id: str
    document_key: str
    document_type: DocumentType
    upload_time: datetime
    metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None

class ReviewRecord(BaseModel):
    """Model for review database records"""
    id: str
    document_id: str
    summary_key: str
    review_key: str
    redlined_key: Optional[str] = None
    issues_count: Dict[str, int]
    processing_time: float
    created_at: datetime

class ComplianceRecord(BaseModel):
    """Model for compliance database records"""
    id: str
    title: str
    summary: str
    source: str
    url: str
    date: datetime
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
