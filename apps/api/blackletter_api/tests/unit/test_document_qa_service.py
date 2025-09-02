from __future__ import annotations

import pytest

from blackletter_api.models.schemas import QASource
from blackletter_api.services.document_qa import (
    DocumentQAService,
    LLMClient,
    VectorStore,
)


class FakeVectorStore(VectorStore):
    def __init__(self) -> None:
        self.last_hybrid: bool | None = None

    async def search(
        self, document_id: str, query: str, *, top_k: int = 5, hybrid: bool = False
    ):
        self.last_hybrid = hybrid
        return [QASource(page=1, content="retrieved chunk")]


class FakeLLM(LLMClient):
    def __init__(self) -> None:
        self.last_question: str | None = None
        self.last_context: str | None = None
        self.last_history: list[str] | None = None

    async def generate(
        self, question: str, context: str, *, chat_history=None
    ) -> str:
        self.last_question = question
        self.last_context = context
        self.last_history = list(chat_history) if chat_history else None
        return f"answer for {question}"


@pytest.mark.asyncio
async def test_answer_simple_uses_vector_store_and_llm() -> None:
    store = FakeVectorStore()
    llm = FakeLLM()
    service = DocumentQAService(store, llm)

    resp = await service.answer_simple("doc1", "What?")

    assert resp.answer == "answer for What?"
    assert resp.sources == []
    assert store.last_hybrid is False
    assert "retrieved chunk" in llm.last_context


@pytest.mark.asyncio
async def test_answer_with_citations_returns_sources() -> None:
    store = FakeVectorStore()
    llm = FakeLLM()
    service = DocumentQAService(store, llm)

    resp = await service.answer_with_citations("doc1", "Where?")

    assert resp.sources[0].page == 1
    assert resp.sources[0].content == "retrieved chunk"
    assert resp.answer == "answer for Where?"


@pytest.mark.asyncio
async def test_answer_with_history_passes_chat_history() -> None:
    store = FakeVectorStore()
    llm = FakeLLM()
    service = DocumentQAService(store, llm)

    history = ["hello", "world"]
    await service.answer_with_history("doc1", "Why?", history)

    assert llm.last_history == history


@pytest.mark.asyncio
async def test_answer_hybrid_uses_hybrid_search() -> None:
    store = FakeVectorStore()
    llm = FakeLLM()
    service = DocumentQAService(store, llm)

    resp = await service.answer_hybrid("doc1", "Hybrid?", ["hi"])

    assert store.last_hybrid is True
    assert resp.sources[0].content == "retrieved chunk"
