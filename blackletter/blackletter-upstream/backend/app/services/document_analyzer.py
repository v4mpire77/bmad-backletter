"""Document Analyzer service following Context Engineering Framework standards.

The analyzer demonstrates multi-modal document extraction by storing raw text
in the RAG store while ensuring structured logging, correlation IDs, and
framework-compliant error handling.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging
import uuid

# Local error and logging utilities replicated from rag_analyzer to avoid heavy imports


class RAGAnalysisError(Exception):
    """Raised when document analysis fails."""


def structured_log(
    logger_instance: logging.Logger,
    level: str,
    message: str,
    correlation_id: str,
    operation: str,
    **kwargs: Any,
) -> None:
    """Simple structured logging helper."""
    log_data = {"correlation_id": correlation_id, "operation": operation, **kwargs}
    getattr(logger_instance, level)(message, extra=log_data)


from .rag_store import rag_store

logger = logging.getLogger(__name__)


@dataclass
class DocumentAnalysisResult:
    """Result object returned after analysis."""
    chunk_count: int


class DocumentAnalyzer:
    """High level document analysis service.

    This class demonstrates how new services should implement structured
    logging, correlation IDs, and framework-compliant error handling.
    """

    async def analyze(self, doc_id: str, text: str, metadata: Dict[str, Any] | None = None) -> DocumentAnalysisResult:
        """Store document text and return analysis metadata.

        Args:
            doc_id: Unique document identifier.
            text: Raw document text to analyse.
            metadata: Optional metadata about the document.

        Returns:
            DocumentAnalysisResult containing the number of chunks stored.

        Raises:
            RAGAnalysisError: If the document cannot be processed.
        """
        if not text or not text.strip():
            raise RAGAnalysisError("No text provided for analysis")

        correlation_id = (metadata or {}).get("correlation_id", str(uuid.uuid4()))
        try:
            structured_log(
                logger,
                "info",
                "storing document in RAG store",
                correlation_id,
                "document_analyze",
                doc_id=doc_id,
            )
            chunks = await rag_store.store_document(doc_id, text, metadata or {})
            structured_log(
                logger,
                "info",
                "document stored",
                correlation_id,
                "document_analyze",
                chunk_count=len(chunks),
            )
            return DocumentAnalysisResult(chunk_count=len(chunks))
        except Exception as exc:  # pragma: no cover - defensive
            error_msg = f"failed to analyze document: {exc}"
            structured_log(logger, "error", error_msg, correlation_id, "document_analyze")
            raise RAGAnalysisError(error_msg) from exc
