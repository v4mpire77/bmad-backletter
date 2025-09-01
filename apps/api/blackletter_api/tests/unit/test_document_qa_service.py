"""Unit tests for DocumentQAService answer methods."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ...services.document_qa import DocumentQAService
from ...models.schemas import QASource


@pytest.mark.asyncio
async def test_answer_simple_uses_placeholders() -> None:
    """Ensure simple RAG returns placeholder answer without sources."""
    service = DocumentQAService()
    service.embedding = MagicMock()
    service.db = MagicMock()
    service.llm = MagicMock()

    result = await service.answer_simple("doc-1", "What is this?")

    assert result.answer == "This is a placeholder answer."
    assert result.sources == []
    service.embedding.assert_not_called()
    service.db.assert_not_called()
    service.llm.assert_not_called()


@pytest.mark.asyncio
async def test_answer_with_citations_returns_source() -> None:
    """RAG with citations should include a source entry."""
    service = DocumentQAService()
    service.embedding = MagicMock()
    service.db = MagicMock()
    service.llm = MagicMock()

    result = await service.answer_with_citations("doc-1", "Question?")

    assert result.answer == "Placeholder answer with citation."
    assert len(result.sources) == 1
    assert isinstance(result.sources[0], QASource)
    service.embedding.assert_not_called()
    service.db.assert_not_called()
    service.llm.assert_not_called()


@pytest.mark.asyncio
async def test_answer_with_history_returns_placeholder() -> None:
    """Conversational RAG should accept chat history and return answer."""
    service = DocumentQAService()
    service.embedding = MagicMock()
    service.db = MagicMock()
    service.llm = MagicMock()

    result = await service.answer_with_history(
        "doc-1", "Question?", chat_history=["hi"]
    )

    assert result.answer == "Placeholder conversational answer."
    assert result.sources == []
    service.embedding.assert_not_called()
    service.db.assert_not_called()
    service.llm.assert_not_called()


@pytest.mark.asyncio
async def test_answer_hybrid_returns_placeholder() -> None:
    """Hybrid search should return placeholder answer."""
    service = DocumentQAService()
    service.embedding = MagicMock()
    service.db = MagicMock()
    service.llm = MagicMock()

    result = await service.answer_hybrid(
        "doc-1", "Question?", chat_history=["hi"]
    )

    assert result.answer == "Placeholder hybrid answer."
    assert result.sources == []
    service.embedding.assert_not_called()
    service.db.assert_not_called()
    service.llm.assert_not_called()

