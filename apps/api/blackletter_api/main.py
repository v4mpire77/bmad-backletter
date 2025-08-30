import os
import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .database import engine, Base
from .models import entities
from .routers import rules, analyses
from .routers import contracts, jobs, reports
from .routers import risk_analysis, admin
from .routers import orchestration, gemini

# Create the database tables
entities.Base.metadata.create_all(bind=engine)

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

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


app = FastAPI(title="Blackletter API", version="0.1.0")

# CORS configuration (allow frontends to call the API)
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(rules.router, prefix="/api")
app.include_router(analyses.router, prefix="/api")
app.include_router(contracts.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(risk_analysis.router, prefix="/api")
app.include_router(admin.router)
app.include_router(orchestration.router)
app.include_router(gemini.router, prefix="/api")


@app.get("/")
def read_root() -> dict[str, bool | str]:
    return {"status": "ok"}


@app.get("/healthz")
def healthz() -> dict[str, bool | str]:
    return {"ok": True}


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
