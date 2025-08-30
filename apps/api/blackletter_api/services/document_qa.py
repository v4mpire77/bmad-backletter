"""Document question-answering service.

Provides multiple retrieval-augmented generation strategies for answering
questions about specific documents. The implementations here are minimal
placeholders that demonstrate the API surface for the four versions described
in the design notes:

1. Simple RAG
2. RAG with citations
3. Conversational RAG with chat history
4. Hybrid semantic/keyword search
"""
from __future__ import annotations

from typing import Iterable, List, Optional

from ..models.schemas import (
    QAResponse,
    QASource,
)


class DocumentQAService:
    """Service for answering questions about uploaded documents.

    The methods currently return placeholder responses. Real implementations
    should integrate a vector store and large language model.
    """

    async def answer_simple(self, document_id: str, question: str) -> QAResponse:
        """Version 1: basic retrieval augmented generation."""
        return QAResponse(answer="This is a placeholder answer.", sources=[])

    async def answer_with_citations(
        self, document_id: str, question: str
    ) -> QAResponse:
        """Version 2: RAG with source citation."""
        source = QASource(page=1, content="Example excerpt")
        return QAResponse(answer="Placeholder answer with citation.", sources=[source])

    async def answer_with_history(
        self,
        document_id: str,
        question: str,
        chat_history: Optional[Iterable[str]] = None,
    ) -> QAResponse:
        """Version 3: conversational RAG using chat history."""
        _ = chat_history  # For future use
        return QAResponse(answer="Placeholder conversational answer.", sources=[])

    async def answer_hybrid(
        self,
        document_id: str,
        question: str,
        chat_history: Optional[Iterable[str]] = None,
    ) -> QAResponse:
        """Version 4: hybrid search (semantic + keyword)."""
        _ = chat_history  # For future use
        return QAResponse(answer="Placeholder hybrid answer.", sources=[])
