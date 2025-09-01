from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Blackletter GDPR Contract Checker"
    DEBUG: bool = False
    API_VERSION: str = "v1"

    # Database configuration
    DATABASE_URL: str

    # Redis configuration for Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Object storage configuration
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: Optional[str] = None  # For Minio/localstack

    # JWT Authentication settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LLM API settings
    OPENAI_API_KEY: str

    # File upload limits
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: list = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    # Pydantic v2 model_config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Create a single, cached instance of the settings
settings = Settings()
