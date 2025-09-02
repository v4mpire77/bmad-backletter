import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Org(Base):
    __tablename__ = "orgs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    members = relationship("OrgMember", back_populates="org")


class OrgMember(Base):
    __tablename__ = "org_members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("orgs.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String(50), nullable=False, default="reviewer")

    org = relationship("Org", back_populates="members")
    user = relationship("User", back_populates="memberships")

