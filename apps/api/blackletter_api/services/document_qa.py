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

from typing import Iterable, List, Optional, Protocol, Sequence

from ..models.schemas import QAResponse, QASource


class VectorStore(Protocol):
    """Minimal vector store protocol used by the service."""

    async def search(
        self,
        document_id: str,
        query: str,
        *,
        top_k: int = 5,
        hybrid: bool = False,
    ) -> Sequence[QASource]:
        ...


class LLMClient(Protocol):
    """Simple large language model interface."""

    async def generate(
        self,
        question: str,
        context: str,
        *,
        chat_history: Optional[Iterable[str]] = None,
    ) -> str:
        ...


class _DummyVectorStore:
    """Fallback vector store that returns no results."""

    async def search(
        self, document_id: str, query: str, *, top_k: int = 5, hybrid: bool = False
    ) -> Sequence[QASource]:
        return []


class _DummyLLMClient:
    """Fallback LLM client returning a placeholder answer."""

    async def generate(
        self,
        question: str,
        context: str,
        *,
        chat_history: Optional[Iterable[str]] = None,
    ) -> str:
        _ = (question, context, chat_history)
        return "This is a placeholder answer."


class DocumentQAService:
    """Service for answering questions about uploaded documents.

    The service relies on a vector store for retrieval and an LLM client for
    answer generation. Default in-memory fallbacks are provided so that the
    service can be instantiated without explicit dependencies (useful for
    tests and the simple router).
    """

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm_client: Optional[LLMClient] = None,
    ) -> None:
        self.vector_store = vector_store or _DummyVectorStore()
        self.llm_client = llm_client or _DummyLLMClient()

    async def _retrieve(
        self, document_id: str, question: str, *, hybrid: bool = False
    ) -> List[QASource]:
        return list(
            await self.vector_store.search(
                document_id, question, top_k=5, hybrid=hybrid
            )
        )

    async def answer_simple(self, document_id: str, question: str) -> QAResponse:
        """Version 1: basic retrieval augmented generation."""
        sources = await self._retrieve(document_id, question)
        context = "\n\n".join(src.content for src in sources)
        answer = await self.llm_client.generate(question, context)
        return QAResponse(answer=answer, sources=[])

    async def answer_with_citations(
        self, document_id: str, question: str
    ) -> QAResponse:
        """Version 2: RAG with source citation."""
        sources = await self._retrieve(document_id, question)
        context = "\n\n".join(src.content for src in sources)
        answer = await self.llm_client.generate(question, context)
        return QAResponse(answer=answer, sources=list(sources))

    async def answer_with_history(
        self,
        document_id: str,
        question: str,
        chat_history: Optional[Iterable[str]] = None,
    ) -> QAResponse:
        """Version 3: conversational RAG using chat history."""
        sources = await self._retrieve(document_id, question)
        context = "\n\n".join(src.content for src in sources)
        answer = await self.llm_client.generate(
            question, context, chat_history=chat_history
        )
        return QAResponse(answer=answer, sources=list(sources))

    async def answer_hybrid(
        self,
        document_id: str,
        question: str,
        chat_history: Optional[Iterable[str]] = None,
    ) -> QAResponse:
        """Version 4: hybrid search (semantic + keyword)."""
        sources = await self._retrieve(document_id, question, hybrid=True)
        context = "\n\n".join(src.content for src in sources)
        answer = await self.llm_client.generate(
            question, context, chat_history=chat_history
        )
        return QAResponse(answer=answer, sources=list(sources))
