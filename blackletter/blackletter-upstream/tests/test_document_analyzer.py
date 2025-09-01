import asyncio
import pytest

from backend.app.services.document_analyzer import DocumentAnalyzer, RAGAnalysisError


def test_analyze_document_stores_chunks():
    analyzer = DocumentAnalyzer()
    result = asyncio.run(analyzer.analyze("doc-1", "Hello world", {"filename": "test.txt"}))
    assert result.chunk_count >= 1


def test_analyze_document_requires_text():
    analyzer = DocumentAnalyzer()
    with pytest.raises(RAGAnalysisError):
        asyncio.run(analyzer.analyze("doc-2", "", {}))
