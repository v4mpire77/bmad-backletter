import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Boolean,
    Float,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base


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
