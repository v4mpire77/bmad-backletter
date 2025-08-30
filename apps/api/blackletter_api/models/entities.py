import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
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


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=False)
    embedding = Column(String, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return (
            f"<DocumentChunk(id={self.id}, document_id='{self.document_id}', "
            f"page_number={self.page_number})>"
        )
