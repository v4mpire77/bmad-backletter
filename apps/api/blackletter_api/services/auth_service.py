import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets

# Use Argon2 for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# Global pepper loaded from environment in production
AUTH_PEPPER = os.getenv("AUTH_PEPPER", "a-super-secret-pepper-from-env")

class AuthService:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password + AUTH_PEPPER, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password + AUTH_PEPPER)

    def create_session_token(self) -> str:
        return secrets.token_urlsafe(32)

    def get_session_expiry(self) -> datetime:
        return datetime.utcnow() + timedelta(days=14)

# Singleton service instance
auth_service = AuthService()
