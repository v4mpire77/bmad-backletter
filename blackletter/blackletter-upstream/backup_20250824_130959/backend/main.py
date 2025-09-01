<<<<<<< HEAD
"""
Blackletter GDPR Processor - Main FastAPI Application
Context Engineering Framework v2.0.0 Compliant
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any

from app.core.config import settings
from app.routers import jobs


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Blackletter GDPR Processor starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Context Engineering Framework compliance required: {settings.framework_compliance_required}%")
    
    yield
    
    # Shutdown
    logger.info("Blackletter GDPR Processor shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Blackletter GDPR Processor",
    description="Context Engineering Framework compliant GDPR Article 28(3) processor obligations checker",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing information."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"Response: {response.status_code} in {process_time:.4f}s")
    
    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with proper error responses."""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with error logging."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": str(request.url)
        }
    )


# Health check endpoints
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for Docker and monitoring."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "framework_compliance": settings.framework_compliance_required,
        "timestamp": time.time()
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Blackletter GDPR Processor API",
        "version": "1.0.0",
        "framework": "Context Engineering Framework v2.0.0",
        "docs": "/docs" if settings.is_development else "Documentation disabled in production"
    }


# Include routers
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])


# Context Engineering Framework compliance check
@app.get("/api/v1/compliance")
async def compliance_check() -> Dict[str, Any]:
    """Context Engineering Framework compliance status."""
    return {
        "framework_version": "2.0.0",
        "required_score": settings.framework_compliance_required,
        "validation_enabled": settings.validation_enabled,
        "status": "compliant" if settings.validation_enabled else "unchecked"
    }
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routers import contracts, dashboard, jobs

app = FastAPI(title="Blackletter Systems API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(contracts.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(
    jobs.router, prefix=f"/api/{settings.API_VERSION}/jobs", tags=["Jobs"]
)


# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
