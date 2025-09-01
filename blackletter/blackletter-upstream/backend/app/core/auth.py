from __future__ import annotations
import os
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import requests
from jose import jwt

logger = logging.getLogger(__name__)

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_JWKS_URL = f"{SUPABASE_PROJECT_URL}/auth/v1/keys" if SUPABASE_PROJECT_URL else ""
SUPABASE_JWT_AUDIENCE = os.getenv("SUPABASE_JWT_AUD", "authenticated")
SUPABASE_JWT_ISSUER = os.getenv("SUPABASE_JWT_ISS", None)

auth_scheme = HTTPBearer(auto_error=True)

_jwks_cache: Optional[dict] = None

def _get_jwks() -> dict:
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache
    if not SUPABASE_JWKS_URL:
        raise RuntimeError("SUPABASE_URL env var not set; cannot fetch JWKS")
    logger.info("Fetching Supabase JWKS from %s", SUPABASE_JWKS_URL)
    resp = requests.get(SUPABASE_JWKS_URL, timeout=5)
    resp.raise_for_status()
    _jwks_cache = resp.json()
    logger.info("Supabase JWKS fetched and cached (keys=%s)", len(_jwks_cache.get("keys", [])))
    return _jwks_cache

def _get_signing_key(token: str):
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    jwks = _get_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signing key")

def verify_supabase_jwt(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    token = credentials.credentials
    try:
        key = _get_signing_key(token)
        claims = jwt.decode(
            token,
            key,
            algorithms=[key.get("alg", "RS256")],
            audience=SUPABASE_JWT_AUDIENCE,
            issuer=SUPABASE_JWT_ISSUER,
            options={"verify_signature": True, "verify_aud": True, "verify_iss": bool(SUPABASE_JWT_ISSUER)},
        )
        user_id = claims.get("sub")
        email = claims.get("email")
        logger.info("Auth success: user_id=%s email=%s audience=%s", user_id, email, SUPABASE_JWT_AUDIENCE)
        return claims
    except Exception as e:
        logger.warning("Auth failed: invalid or expired token (%s)", str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from e


