"""
Blackletter GDPR Processor - Core Configuration
Context Engineering Framework v2.0.0 Compliant
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable loading."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Supabase Configuration
    supabase_url: str = "https://your-project.supabase.co"
    supabase_service_key: str = "your-service-key"
    supabase_anon_key: str = "your-anon-key"
    database_url: str = "postgresql://postgres:password@localhost:5432/blackletter"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # FastAPI Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    
    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # LLM Configuration (Optional for MVP)
    llm_provider: str = "openai"
    llm_model: str = "gpt-4"
    openai_api_key: Optional[str] = None
    
    # Application Settings
    max_upload_size: int = 10485760  # 10MB
    allowed_file_types: List[str] = ["pdf", "txt", "docx"]
    job_timeout_seconds: int = 300
    
    # Context Engineering Framework
    framework_compliance_required: int = 80
    validation_enabled: bool = True
    
    # Development Settings
    debug: bool = False
    log_level: str = "INFO"
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Testing
    testing: bool = False
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.testing


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Export settings instance
settings = get_settings()