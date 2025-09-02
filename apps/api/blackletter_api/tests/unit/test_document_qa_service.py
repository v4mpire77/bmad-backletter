import pytest
from unittest.mock import AsyncMock

from blackletter_api.services.document_qa import DocumentQAService
from blackletter_api.models.schemas import QASource


@pytest.mark.asyncio
async def test_answer_simple_uses_vector_store_and_llm() -> None:
    vector_store = AsyncMock()
    vector_store.search.return_value = [QASource(page=1, content="chunk")]
    llm = AsyncMock()
    llm.generate.return_value = "final answer"
    service = DocumentQAService(vector_store=vector_store, llm=llm)

    res = await service.answer_simple("doc", "question")

    assert res.answer == "final answer"
    assert res.sources == []
    vector_store.search.assert_awaited_once()
    llm.generate.assert_awaited_once()


@pytest.mark.asyncio
async def test_answer_with_citations_returns_sources() -> None:
    src = QASource(page=2, content="evidence")
    vector_store = AsyncMock()
    vector_store.search.return_value = [src]
    llm = AsyncMock()
    llm.generate.return_value = "answer"
    service = DocumentQAService(vector_store=vector_store, llm=llm)

    res = await service.answer_with_citations("doc", "question")

    assert res.sources == [src]
    vector_store.search.assert_awaited_once()


@pytest.mark.asyncio
async def test_answer_with_history_includes_chat_history() -> None:
    vector_store = AsyncMock()
    vector_store.search.return_value = []
    llm = AsyncMock()
    llm.generate.return_value = "answer"
    service = DocumentQAService(vector_store=vector_store, llm=llm)

    await service.answer_with_history("doc", "question", ["hi there"])

    prompt = llm.generate.call_args[0][0]
    assert "hi there" in prompt


@pytest.mark.asyncio
async def test_answer_hybrid_combines_search_results() -> None:
    sem = QASource(page=1, content="sem")
    kw = QASource(page=2, content="kw")
    vector_store = AsyncMock()
    vector_store.search.return_value = [sem]
    vector_store.keyword_search.return_value = [kw]
    llm = AsyncMock()
    llm.generate.return_value = "answer"
    service = DocumentQAService(vector_store=vector_store, llm=llm)

    res = await service.answer_hybrid("doc", "question")

    pages = {s.page for s in res.sources}
    assert pages == {1, 2}
    vector_store.search.assert_awaited_once()
    vector_store.keyword_search.assert_awaited_once()
