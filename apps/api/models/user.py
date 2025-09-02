from __future__ import annotations

from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from passlib.context import CryptContext

Base = declarative_base()

# Use an in-memory SQLite database shared across the application for tests
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(Base):
    """Represents a role a user can have."""

    __tablename__ = "roles"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class Organization(Base):
    """Company or organization grouping users."""

    __tablename__ = "organizations"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="organization")


class User(Base):
    """Application user with hashed password support."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    role_id: Optional[int] = Column(Integer, ForeignKey("roles.id"))
    organization_id: Optional[int] = Column(Integer, ForeignKey("organizations.id"))

    role = relationship("Role", back_populates="users")
    organization = relationship("Organization", back_populates="users")

    def set_password(self, password: str) -> None:
        """Hash and store the given password."""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return pwd_context.verify(password, self.hashed_password)


# Create tables for the models when imported
Base.metadata.create_all(bind=engine)
