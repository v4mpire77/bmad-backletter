"""Authentication routes for the Blackletter API."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..auth import authenticate_user, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(req: LoginRequest):
    """Authenticate a user and return a JWT access token."""
    if not authenticate_user(req.username, req.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(req.username)
    return {"access_token": token}
