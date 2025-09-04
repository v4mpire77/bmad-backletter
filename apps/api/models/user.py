from enum import Enum
from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    """Enumeration of application roles."""

    ADMIN = "admin"
    REVIEWER = "reviewer"


class User(BaseModel):
    """Application user with an associated role."""

    id: str
    email: EmailStr
    role: Role
