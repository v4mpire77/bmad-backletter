"""Simple authentication utilities for the Blackletter API."""
import os
from datetime import datetime, timedelta
from typing import Dict

import jwt

# Demo in-memory user store
_USER_DB: Dict[str, str] = {"user@example.com": "strongPassword"}

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def authenticate_user(username: str, password: str) -> bool:
    """Validate a user's credentials against the in-memory store."""
    expected = _USER_DB.get(username)
    return expected is not None and expected == password

def create_access_token(username: str) -> str:
    """Create a signed JWT access token for a given username."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
