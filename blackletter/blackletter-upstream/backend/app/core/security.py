"""
Security Module for Blackletter Systems

Provides comprehensive security features including:
- Rate limiting
- Input validation and sanitization
- File upload security
- Request validation
"""

import re
import hashlib
import time
from typing import Dict, List, Optional, Tuple
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
import logging
from pathlib import Path
import magic
import mimetypes

logger = logging.getLogger(__name__)

from .threat_detection import threat_detection_service
from .security_config import security_config

# Security configuration
MAX_REQUESTS_PER_MINUTE = 60
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = {
    'application/pdf': ['.pdf'],
    'text/plain': ['.txt'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/msword': ['.doc'],
}

# Rate limiting storage (use Redis in production)
request_counts: Dict[str, List[float]] = {}

class SecurityMiddleware:
    """Security middleware for request validation and rate limiting"""
    
    @staticmethod
    def validate_rate_limit(client_ip: str) -> bool:
        """Check if client has exceeded rate limit"""
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old requests
        if client_ip in request_counts:
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip] 
                if req_time > minute_ago
            ]
        else:
            request_counts[client_ip] = []
        
        # Check limit
        if len(request_counts[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return False
        
        # Add current request
        request_counts[client_ip].append(current_time)
        return True
    
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """Extract client IP from request headers"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"

    @staticmethod
    def analyze_request(request: Request) -> None:
        """Run ML-based threat analysis on the request."""
        if not security_config.ENABLE_THREAT_DETECTION:
            return

        client_ip = SecurityMiddleware.get_client_ip(request)
        session_id = request.headers.get("X-Session-ID") or request.cookies.get(
            "session_id", "anonymous"
        )
        payload_size = int(request.headers.get("Content-Length") or 0)

        score = threat_detection_service.analyze_request(
            client_ip=client_ip,
            path=request.url.path,
            method=request.method,
            user_agent=request.headers.get("User-Agent", ""),
            payload_size=payload_size,
            session_id=session_id,
        )

        if score >= security_config.THREAT_SCORE_THRESHOLD:
            logger.warning(
                "Blocking request from %s with high threat score %.2f", client_ip, score
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Suspicious activity detected",
            )
    
    @staticmethod
    def validate_file_upload(file_content: bytes, filename: str, content_type: str) -> Tuple[bool, str]:
        """
        Comprehensive file upload validation
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # File size validation
            if len(file_content) > MAX_FILE_SIZE:
                return False, f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            
            # File type validation
            if not SecurityMiddleware._is_allowed_file_type(filename, content_type, file_content):
                return False, "File type not allowed or content mismatch detected"
            
            # Filename security
            if not SecurityMiddleware._is_safe_filename(filename):
                return False, "Filename contains potentially dangerous characters"
            
            # Content validation
            if not SecurityMiddleware._validate_file_content(file_content, content_type):
                return False, "File content validation failed"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False, "File validation failed"
    
    @staticmethod
    def _is_allowed_file_type(filename: str, content_type: str, file_content: bytes) -> bool:
        """Check if file type is allowed"""
        # Check extension
        file_ext = Path(filename).suffix.lower()
        if not any(file_ext in exts for exts in ALLOWED_FILE_TYPES.values()):
            return False
        
        # Check MIME type
        if content_type not in ALLOWED_FILE_TYPES:
            return False
        
        # Verify content matches declared type
        try:
            detected_type = magic.from_buffer(file_content, mime=True)
            if detected_type != content_type:
                logger.warning(f"Content type mismatch: declared={content_type}, detected={detected_type}")
                return False
        except Exception:
            # Fallback to extension-based validation
            pass
        
        return True
    
    @staticmethod
    def _is_safe_filename(filename: str) -> bool:
        """Check if filename is safe (no path traversal, etc.)"""
        # Check for path traversal attempts
        dangerous_patterns = [
            r'\.\.',  # Directory traversal
            r'/',     # Path separators
            r'\\',    # Windows path separators
            r'[<>:"|?*]',  # Invalid characters
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, filename):
                return False
        
        # Check length
        if len(filename) > 255:
            return False
        
        return True
    
    @staticmethod
    def _validate_file_content(file_content: bytes, content_type: str) -> bool:
        """Validate file content based on type"""
        try:
            if content_type == 'text/plain':
                # Check if content is valid UTF-8
                file_content.decode('utf-8')
            elif content_type == 'application/pdf':
                # Check PDF magic number
                if not file_content.startswith(b'%PDF'):
                    return False
            elif content_type.startswith('application/vnd.openxmlformats-officedocument'):
                # Check Office document magic numbers
                if not (file_content.startswith(b'PK') or file_content.startswith(b'\xd0\xcf\x11\xe0')):
 return False # OLE2 compound document signature for .doc files
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """Sanitize user input text"""
        if not text:
            return ""
        
        # Remove null bytes and control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limit length
        if len(text) > max_length:
            text = text[:max_length]
        
        # Basic XSS protection
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
        ]
        
        for pattern in dangerous_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        return text.strip()
    
    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """Validate UUID format"""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(uuid_string))
    
    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """Generate a secure filename with hash"""
        # Extract extension
        ext = Path(original_filename).suffix.lower()
        
        # Generate hash from original name and timestamp
        hash_input = f"{original_filename}{time.time()}"
        file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        
        return f"{file_hash}{ext}"

# Rate limiting decorator
def rate_limit(max_requests: int = MAX_REQUESTS_PER_MINUTE):
    """Decorator to apply rate limiting to endpoints"""
    def decorator(func):
        async def wrapper(*args, request: Request = None, **kwargs):
            if request:
                client_ip = SecurityMiddleware.get_client_ip(request)
                if not SecurityMiddleware.validate_rate_limit(client_ip):
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Please try again later."
                    )
                # Run ML-based threat detection
                SecurityMiddleware.analyze_request(request)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# File validation decorator
def validate_file_upload():
    """Decorator to validate file uploads"""
    def decorator(func):
        async def wrapper(*args, file=None, **kwargs):
            if file:
                is_valid, error_msg = SecurityMiddleware.validate_file_upload(
                    await file.read(),
                    file.filename or "",
                    file.content_type or ""
                )
                if not is_valid:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=error_msg
                    )
                # Reset file position for actual processing
                await file.seek(0)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
