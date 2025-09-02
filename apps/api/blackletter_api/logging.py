import os
import time
import logging
from logging.config import dictConfig
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


def setup_logging() -> None:
    """Configure application logging.

    Uses environment variables LOG_LEVEL and LOG_FORMAT to switch between
    plain text and JSON output. Uvicorn access logs are disabled so all HTTP
    traffic flows through our structured middleware.
    """
    log_level = os.getenv("LOG_LEVEL", "info").upper()
    log_format = os.getenv("LOG_FORMAT", "plain").lower()

    if log_format == "json":
        formatter: dict[str, Any] = {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
        }
    else:
        formatter = {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}

    dictConfig(
        {
            "version": 1,
            "formatters": {"default": formatter},
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {"level": log_level, "handlers": ["default"]},
        }
    )
    logging.getLogger("uvicorn.access").disabled = True


class LogMiddleware(BaseHTTPMiddleware):
    """Emit a structured log for each HTTP request/response pair."""

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        start = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000
        logging.getLogger(__name__).info(
            "request",
            extra={
                "req": {"method": request.method, "path": request.url.path},
                "res": {"status_code": response.status_code},
                "duration_ms": round(duration_ms, 2),
            },
        )
        return response
