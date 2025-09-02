"""
Configuration settings for Blackletter API
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database settings
    database_url: str = Field(default="sqlite:///./blackletter.db", env="DATABASE_URL")

    # CORS settings
    cors_origins: str = Field(default="*", env="CORS_ORIGINS")

    # Gemini AI settings
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-flash", env="GEMINI_MODEL")
    gemini_max_tokens: int = Field(default=2048, env="GEMINI_MAX_TOKENS")
    gemini_temperature: float = Field(default=0.7, env="GEMINI_TEMPERATURE")

    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Security settings
    secret_key: str = Field(..., env="SECRET_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
