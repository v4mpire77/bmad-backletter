"""FastAPI router exports for convenience."""

from . import contracts, dashboard, gemini, jobs, ocr, rag

__all__ = [
    "contracts",
    "dashboard",
    "gemini",
    "ocr",
    "rag",
    "jobs",
]
