from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest) -> TokenResponse:
    """Validate credentials and return a stubbed token."""
    if data.username == "admin" and data.password == "password":
        return TokenResponse(access_token="fake-token")
    raise HTTPException(status_code=401, detail="invalid_credentials")
