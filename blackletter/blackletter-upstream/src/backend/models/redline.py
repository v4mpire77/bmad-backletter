from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Text, func

from ..database import Base


class Redline(Base):
    __tablename__ = "redlines"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(String, nullable=False, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
