"""Blackletter API - Main application entrypoint (Sprint 1 vertical slice)

This file sets up a minimal FastAPI application with structured logging,
request metrics middleware, and simple health/readiness endpoints.
"""

import os
import uuid
import logging
import time
import json
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .database import engine, Base
from .models import entities
from .routers import rules, analyses, findings, analysis
from .routers import contracts, jobs, reports
from .routers import docs, exports
from .routers import risk_analysis, admin
from .routers import orchestration, gemini
from .routers import document_qa
from .routers import auth, devtools, settings, organizations

# Create the database tables
entities.Base.metadata.create_all(bind=engine)

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        dead_connections: List[WebSocket] = []
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as exc:
                logger.warning(f"Failed to send message: {exc}")
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(connection)

manager = ConnectionManager()

# --- Structured Logging Setup ---

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'job_id'):
            log_record['job_id'] = record.job_id
        if hasattr(record, 'analysis_id'):
            log_record['analysis_id'] = record.analysis_id
        if hasattr(record, 'latency_ms'):
            log_record['latency_ms'] = record.latency_ms
        
        return json.dumps(log_record)

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove existing handlers and add our JSON formatter
if logger.hasHandlers():
    logger.handlers.clear()
logHandler = logging.StreamHandler()
logHandler.setFormatter(JsonFormatter())
logger.addHandler(logHandler)

# --- End Logging Setup ---


app = FastAPI(
    title="Blackletter Systems API",
    description="API for GDPR contract analysis.",
    version="0.1.0"
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return errors in a consistent JSON envelope."""

    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": "error", "message": str(exc.detail)},
    )


@app.middleware("http")
async def add_process_time_header_and_logging(request: Request, call_next):
    """
    Middleware to add a correlation ID, log requests, and measure latency.
    This fulfills parts of E4 (Metrics & Observability) for Sprint 1.
    """
    start_time = time.time()
    correlation_id = str(uuid.uuid4())

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    logger.info(
        f'{{"correlation_id": "{correlation_id}", "method": "{request.method}", '
        f'"path": "{request.url.path}", "status_code": {response.status_code}, '
        f'"duration_ms": {process_time:.2f}}}'
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return response


# E4: Health and Readiness Endpoints
@app.get("/healthz", tags=["Health"])
async def get_health():
    """
    Simple health check. Returns OK if the server is running.
    """
    return JSONResponse(content={"ok": True})


@app.get("/readyz", tags=["Health"])
async def get_readiness():
    """Perform a simple database connectivity check."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503, content={"ok": False, "db": "error"}
        )
    return JSONResponse(content={"ok": True, "db": "ok", "migrations": "ok"})


@app.get("/")
def read_root() -> dict[str, bool | str]:
    return {"status": "ok"}


@app.websocket("/ws/analysis/{analysis_id}")
async def websocket_endpoint(websocket: WebSocket, analysis_id: str):
    await manager.connect(websocket)
    try:
        # Send initial connection confirmation
        await manager.send_personal_message(
            json.dumps({
                "type": "connection",
                "analysis_id": analysis_id,
                "message": "Connected to real-time analysis updates"
            }), 
            websocket
        )
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Echo back for now, could be used for control messages
            await manager.send_personal_message(
                json.dumps({
                    "type": "echo",
                    "analysis_id": analysis_id,
                    "data": data
                }), 
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/api/analysis/{analysis_id}/live")
async def get_live_analysis_status(analysis_id: str):
    """Get real-time status of an analysis with live updates capability"""
    return {
        "analysis_id": analysis_id,
        "websocket_url": f"/ws/analysis/{analysis_id}",
        "status": "live",
        "message": "Connect to WebSocket for real-time updates"
    }
app.include_router(rules.router, prefix="/api")
app.include_router(analyses.router, prefix="/api")
app.include_router(findings.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(contracts.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(risk_analysis.router, prefix="/api")
app.include_router(admin.router)
app.include_router(orchestration.router)
app.include_router(gemini.router, prefix="/api")
app.include_router(document_qa.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(devtools.router, prefix="/api/dev")
app.include_router(settings.router)
app.include_router(organizations.router, prefix="/api")

# V1 prefixed routes
app.include_router(contracts.router, prefix="/v1")
app.include_router(docs.router, prefix="/v1")
app.include_router(exports.router, prefix="/v1")
