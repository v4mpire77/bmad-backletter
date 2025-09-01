import uuid

from sqlalchemy import JSON, Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..db.session import Base
from .schemas import ContractType, JobStatus, Jurisdiction


class Job(Base):
    __tablename__ = "jobs"

    # Core Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(
        SQLAlchemyEnum(JobStatus, name="job_status_enum"),
        nullable=False,
        default=JobStatus.QUEUED,
        index=True,
    )

    # Input Parameters
    file_object_key = Column(
        String,
        nullable=False,
        unique=True,
        comment="The key of the file in the object store (e.g., S3).",
    )
    original_filename = Column(String, nullable=False)
    contract_type = Column(
        SQLAlchemyEnum(ContractType, name="contract_type_enum"),
        nullable=False,
        index=True,
    )
    jurisdiction = Column(
        SQLAlchemyEnum(Jurisdiction, name="jurisdiction_enum"),
        nullable=False,
        index=True,
    )
    playbook_id = Column(String, nullable=True, index=True)

    # Processing metadata
    file_size = Column(Integer, nullable=True)
    extracted_text_length = Column(Integer, nullable=True)
    processing_steps_completed = Column(JSON, nullable=True, default=list)

    # Output and Error Handling
    result = Column(
        JSON,
        nullable=True,
        comment="The detailed analysis result stored as a JSON object.",
    )
    report_file_key = Column(
        String,
        nullable=True,
        comment="S3 key for the generated PDF report.",
    )
    error_message = Column(String, nullable=True)
    processing_time_seconds = Column(Float, nullable=True)

    # Auditing and Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Multi-tenancy support (uncomment when needed)
    # tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    # user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
