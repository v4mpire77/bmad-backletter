"""
Security Configuration for Blackletter Systems

Environment-based security settings and configurations.
"""

import os
from typing import List, Dict, Any

class SecurityConfig:
    """Security configuration class"""
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"
    
    # CORS Configuration
    ALLOWED_ORIGINS = {
        "production": [
            "https://blackletter-frontend.onrender.com",
            "https://blackletter-systems.onrender.com",
            "https://blackletter.vercel.app",
        ],
        "development": [
            "http://localhost:3000",
            "http://localhost:3001",
        ]
    }
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_BURST_SIZE = int(os.getenv("RATE_LIMIT_BURST_SIZE", "10"))
    
    # File Upload Security
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", "10")) * 1024 * 1024  # Convert MB to bytes
    ALLOWED_FILE_TYPES = {
        'application/pdf': ['.pdf'],
        'text/plain': ['.txt'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/msword': ['.doc'],
    }
    
    # Authentication
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Session Security
    SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "strict"
    
    # Security Headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains" if ENVIRONMENT == "production" else None,
    }
    
    # Trusted Hosts (Production only)
    TRUSTED_HOSTS = {
        "production": [
            "blackletter-frontend.onrender.com",
            "blackletter-systems.onrender.com", 
            "blackletter.vercel.app",
        ],
        "development": ["*"]
    }
    
    # Input Validation
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", "1000"))
    MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "500"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_SECURITY_EVENTS = os.getenv("LOG_SECURITY_EVENTS", "true").lower() == "true"

    # Threat Detection
    ENABLE_THREAT_DETECTION = os.getenv(
        "ENABLE_THREAT_DETECTION", "true"
    ).lower() == "true"
    THREAT_SCORE_THRESHOLD = float(os.getenv("THREAT_SCORE_THRESHOLD", "0.7"))
    
    # Monitoring
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_RETENTION_DAYS = int(os.getenv("METRICS_RETENTION_DAYS", "30"))
    
    @classmethod
    def get_allowed_origins(cls) -> List[str]:
        """Get allowed origins for current environment"""
        return cls.ALLOWED_ORIGINS.get(cls.ENVIRONMENT, cls.ALLOWED_ORIGINS["development"])
    
    @classmethod
    def get_trusted_hosts(cls) -> List[str]:
        """Get trusted hosts for current environment"""
        return cls.TRUSTED_HOSTS.get(cls.ENVIRONMENT, cls.TRUSTED_HOSTS["development"])
    
    @classmethod
    def get_security_headers(cls) -> Dict[str, str]:
        """Get security headers for current environment"""
        headers = {}
        for key, value in cls.SECURITY_HEADERS.items():
            if value is not None:
                headers[key] = value
        return headers
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT == "development"

# Global security configuration instance
security_config = SecurityConfig()

