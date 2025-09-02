import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Boolean,
    Float,
    Enum,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
import enum


class LLMProvider(enum.Enum):
    """Enum for LLM provider options in Story 5.1."""
    none = "none"
    openai = "openai"
    anthropic = "anthropic"
    gemini = "gemini"


class RetentionPolicy(enum.Enum):
    """Enum for retention policy options in Story 5.1."""
    none = "none"
    thirty_days = "30d"
    ninety_days = "90d"


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="queued")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    # org_id is not used in MVP, but good to have for future multi-tenancy
    org_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<Analysis(id={self.id}, filename='{self.filename}', status='{self.status}')>"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    status = Column(String, nullable=False, default="queued")
    error_reason = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Job(id={self.id}, status='{self.status}')>"


# Minimal Document model with tenancy scope
class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    org_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}')>"


# Minimal Finding model with tenancy scope
class Finding(Base):
    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    org_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    rule = Column(String, nullable=False)
    detail = Column(String, nullable=True)

    def __repr__(self):
        return f"<Finding(id={self.id}, rule='{self.rule}')>"


# Story 2.4 - Metric model for token tracking and metrics
class Metric(Base):
    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    tokens_per_doc = Column(Integer, nullable=False, default=0)
    llm_invoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Additional metrics fields for comprehensive tracking
    processing_time_ms = Column(Float, nullable=True)
    detection_count = Column(Integer, nullable=False, default=0)
    error_reason = Column(String, nullable=True)  # For token_cap, extraction_failed, etc.
    
    def __repr__(self):
        return f"<Metric(id={self.id}, analysis_id={self.analysis_id}, tokens={self.tokens_per_doc}, llm={self.llm_invoked})>"


# Story 5.1 - Organization Settings model
class OrgSetting(Base):
    __tablename__ = "org_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False, index=True, default=uuid.uuid4)  # Default org for MVP
    
    # Story 5.1 settings fields
    llm_provider = Column(Enum(LLMProvider), nullable=False, default="none")
    ocr_enabled = Column(Boolean, nullable=False, default=False)
    retention_policy = Column(Enum(RetentionPolicy), nullable=False, default="none")
    
    # Audit fields
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<OrgSetting(id={self.id}, org_id={self.org_id}, llm_provider={self.llm_provider.value})>"
