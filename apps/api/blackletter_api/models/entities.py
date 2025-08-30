import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
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
    # For auditability, persist the rulepack id/version used for this analysis (e.g., "art28_v1")
    rulepack_version = Column(String, nullable=False, default="art28_v1")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    # org_id is not used in MVP, but good to have for future multi-tenancy
    org_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<Analysis(id={self.id}, filename='{self.filename}', status='{self.status}')>"
