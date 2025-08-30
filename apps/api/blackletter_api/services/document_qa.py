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

from typing import Callable, Iterable, List, Optional

from ..models.schemas import (
    QAResponse,
    QASource,
)
from .gemini_service import gemini_service


class DocumentQAService:
    """Service for answering questions about uploaded documents.

    The service uses dependency-injected embedding and LLM callables so the
    implementation can be easily swapped for tests. If not provided, sensible
    defaults are used:

    * ``embed_fn`` – uses a small sentence-transformer via LangChain
    * ``llm_fn`` – calls the configured :class:`GeminiService` client
    """

    def __init__(
        self,
        embed_fn: Callable[[str], List[float]] | None = None,
        llm_fn: Callable[[str], str] | None = None,
    ) -> None:
        self._embed = embed_fn or self._default_embed
        self._call_llm = llm_fn or self._default_call_llm

    # ------------------------------------------------------------------
    # Default dependency implementations
    # ------------------------------------------------------------------
    def _default_embed(self, text: str) -> List[float]:
        """Generate an embedding for ``text`` using LangChain.

        The model is instantiated lazily so tests can inject a cheap stub
        without pulling heavy weights.
        """

        try:
            from langchain.embeddings import HuggingFaceEmbeddings
        except Exception:  # pragma: no cover - optional dependency
            return [0.0]

        if not hasattr(self, "_embedder"):
            self._embedder = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        return self._embedder.embed_query(text)

    def _default_call_llm(self, prompt: str) -> str:
        """Call the deployed LLM client with ``prompt``."""

        if not gemini_service.is_available():
            return "LLM service unavailable"
        try:
            response = gemini_service.model.generate_content(prompt)
        except Exception:  # pragma: no cover - network/LLM errors
            return "LLM request failed"
        return getattr(response, "text", str(response))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    async def answer_simple(self, document_id: str, question: str) -> QAResponse:
        """Version 1: basic retrieval augmented generation."""

        answer = self._call_llm(question)
        return QAResponse(answer=answer, sources=[])

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
