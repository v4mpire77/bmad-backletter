"""Document question‑answering service."""

from __future__ import annotations

from typing import Iterable, List, Optional, Protocol

from ..models.schemas import QAResponse, QASource


class VectorStore(Protocol):
    """Protocol for vector store search implementations."""

    async def search(
        self, document_id: str, query: str, top_k: int = 4
    ) -> List[QASource]:
        """Semantic search over document chunks."""

    async def keyword_search(
        self, document_id: str, query: str, top_k: int = 4
    ) -> List[QASource]:
        """Optional keyword search used by the hybrid mode."""


class LLMClient(Protocol):
    """Protocol for text completion APIs."""

    async def generate(self, prompt: str) -> str:
        """Return the model's completion for ``prompt``."""


class DummyVectorStore:
    """Fallback vector store returning a canned chunk.

    This keeps the router working in environments where no real vector store
    is configured.
    """

    async def search(self, document_id: str, query: str, top_k: int = 4) -> List[QASource]:
        return [QASource(page=1, content="Example excerpt")]

    async def keyword_search(
        self, document_id: str, query: str, top_k: int = 4
    ) -> List[QASource]:
        return []


class DummyLLM:
    """Fallback LLM client returning a placeholder answer."""

    async def generate(self, prompt: str) -> str:  # pragma: no cover - trivial
        return "This is a placeholder answer."


class DocumentQAService:
    """Service for answering questions about uploaded documents."""

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm: Optional[LLMClient] = None,
    ) -> None:
        self.vector_store = vector_store or DummyVectorStore()
        self.llm = llm or DummyLLM()

    async def _retrieve_semantic(
        self, document_id: str, question: str, top_k: int = 4
    ) -> List[QASource]:
        return await self.vector_store.search(document_id, question, top_k)

    async def _retrieve_keyword(
        self, document_id: str, question: str, top_k: int = 4
    ) -> List[QASource]:
        return await self.vector_store.keyword_search(document_id, question, top_k)

    def _build_prompt(
        self,
        question: str,
        sources: List[QASource],
        chat_history: Optional[Iterable[str]] = None,
    ) -> str:
        context = "\n".join(src.content for src in sources)
        history_section = (
            "Chat History:\n" + "\n".join(chat_history) + "\n"
            if chat_history
            else ""
        )
        return f"{history_section}Context:\n{context}\nQuestion: {question}"

    async def _ask_llm(self, prompt: str) -> str:
        return await self.llm.generate(prompt)

    async def answer_simple(self, document_id: str, question: str) -> QAResponse:
        """Version 1: basic retrieval augmented generation."""
        sources = await self._retrieve_semantic(document_id, question)
        prompt = self._build_prompt(question, sources)
        answer = await self._ask_llm(prompt)
        return QAResponse(answer=answer, sources=[])

    async def answer_with_citations(
        self, document_id: str, question: str
    ) -> QAResponse:
        """Version 2: RAG with source citation."""
        sources = await self._retrieve_semantic(document_id, question)
        prompt = self._build_prompt(question, sources)
        answer = await self._ask_llm(prompt)
        return QAResponse(answer=answer, sources=sources)

    async def answer_with_history(
        self,
        document_id: str,
        question: str,
        chat_history: Optional[Iterable[str]] = None,
    ) -> QAResponse:
        """Version 3: conversational RAG using chat history."""
        sources = await self._retrieve_semantic(document_id, question)
        prompt = self._build_prompt(question, sources, chat_history)
        answer = await self._ask_llm(prompt)
        return QAResponse(answer=answer, sources=sources)

    async def answer_hybrid(
        self,
        document_id: str,
        question: str,
        chat_history: Optional[Iterable[str]] = None,
    ) -> QAResponse:
        """Version 4: hybrid search (semantic + keyword)."""
        semantic_sources = await self._retrieve_semantic(document_id, question)
        keyword_sources = await self._retrieve_keyword(document_id, question)
        # De‑duplicate by page/content pair to avoid repeats
        combined_dict = {
            (src.page, src.content): src for src in (*semantic_sources, *keyword_sources)
        }
        combined_sources = list(combined_dict.values())
        prompt = self._build_prompt(question, combined_sources, chat_history)
        answer = await self._ask_llm(prompt)
        return QAResponse(answer=answer, sources=combined_sources)
