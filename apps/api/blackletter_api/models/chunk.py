from __future__ import annotations

from sqlalchemy import Column, Integer, Text

from ..database import Base


class DocumentChunk(Base):
    """Persistence model for document text chunks."""

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
