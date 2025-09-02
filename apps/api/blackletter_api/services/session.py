from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

SECRET_KEY = os.getenv("JWT_SECRET", "test-secret")
ALGORITHM = "HS256"
DEFAULT_EXPIRATION = timedelta(minutes=30)


def create_session_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a signed JWT for the given subject."""
    expire = datetime.utcnow() + (expires_delta or DEFAULT_EXPIRATION)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_session_token(token: str) -> Optional[str]:
    """Verify a session token and return the subject if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
