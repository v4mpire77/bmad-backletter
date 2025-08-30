import os
import logging
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .models import entities
from .routers import rules, analyses
from .routers import contracts, jobs, reports

# Create the database tables
entities.Base.metadata.create_all(bind=engine)

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


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/healthz")
def healthz():
    return {"ok": True}
