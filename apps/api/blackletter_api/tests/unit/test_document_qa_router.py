from typing import List, Optional
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from blackletter_api.routers.document_qa import router as qa_router
from blackletter_api.models.schemas import QAResponse, QASource
from blackletter_api.services.document_qa import DocumentQAService

app = FastAPI()
app.include_router(qa_router, prefix="/api")
client = TestClient(app)


def test_document_qa_simple() -> None:
    res = client.post(
        "/api/documents/doc-1/qa",
        json={"question": "What is the purpose?"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"]
    assert data["sources"] == []

def _mock_embed(self, text: str) -> List[float]:
    return [0.1, 0.2, 0.3]

def _mock_vector_search(
    self, document_id: str, embedding: List[float]
) -> List[QASource]:
    return [
        QASource(page=1, content="Clause A"),
        QASource(page=1, content="Clause A"),
        QASource(page=2, content="Clause B"),
    ]

def _mock_call_llm(self, question: str, docs: List[QASource | str]) -> str:
    return "deterministic answer"

async def _mock_answer_simple(self, document_id: str, question: str) -> QAResponse:
    self._embed(question)
    docs = self._vector_search(document_id, [])
    answer = self._call_llm(question, docs)
    return QAResponse(answer=answer, sources=[])

async def _mock_answer_with_citations(
    self, document_id: str, question: str
) -> QAResponse:
    self._embed(question)
    docs = self._vector_search(document_id, [])
    answer = self._call_llm(question, docs)
    return QAResponse(answer=answer, sources=docs[:1])

async def _mock_answer_with_history(
    self, document_id: str, question: str, chat_history: Optional[List[str]] = None
) -> QAResponse:
    self._embed(question)
    docs = self._vector_search(document_id, [])
    answer = self._call_llm(question, chat_history or docs)
    return QAResponse(answer=answer, sources=[])

async def _mock_answer_hybrid(
    self, document_id: str, question: str, chat_history: Optional[List[str]] = None
) -> QAResponse:
    self._embed(question)
    docs = self._vector_search(document_id, [])
    unique = {(s.page, s.content): s for s in docs}
    answer = self._call_llm(question, list(unique.values()))
    return QAResponse(answer=answer, sources=list(unique.values()))

def test_qa_v1_simple() -> None:
    with patch.object(DocumentQAService, "_embed", _mock_embed, create=True),         patch.object(DocumentQAService, "_vector_search", _mock_vector_search, create=True),         patch.object(DocumentQAService, "_call_llm", _mock_call_llm, create=True),         patch.object(DocumentQAService, "answer_simple", _mock_answer_simple):
        res = client.post("/api/documents/doc-1/qa", json={"question": "Q?"})
        assert res.status_code == 200
        assert res.json() == {"answer": "deterministic answer", "sources": []}

def test_qa_v2_citations() -> None:
    with patch.object(DocumentQAService, "_embed", _mock_embed, create=True),         patch.object(DocumentQAService, "_vector_search", _mock_vector_search, create=True),         patch.object(DocumentQAService, "_call_llm", _mock_call_llm, create=True),         patch.object(DocumentQAService, "answer_with_citations", _mock_answer_with_citations):
        res = client.post(
            "/api/documents/doc-1/qa",
            json={"question": "Q?", "mode": "citations"},
        )
        assert res.status_code == 200
        assert res.json() == {
            "answer": "deterministic answer",
            "sources": [{"page": 1, "content": "Clause A"}],
        }

def test_qa_v3_conversational_missing_history() -> None:
    with patch.object(DocumentQAService, "_embed", _mock_embed, create=True),         patch.object(DocumentQAService, "_vector_search", _mock_vector_search, create=True),         patch.object(DocumentQAService, "_call_llm", _mock_call_llm, create=True),         patch.object(DocumentQAService, "answer_with_history", _mock_answer_with_history):
        res = client.post(
            "/api/documents/doc-1/qa",
            json={"question": "Q?", "mode": "conversational"},
        )
        assert res.status_code == 200
        assert res.json() == {"answer": "deterministic answer", "sources": []}

def test_qa_v4_hybrid_keyword_overlap() -> None:
    with patch.object(DocumentQAService, "_embed", _mock_embed, create=True),         patch.object(DocumentQAService, "_vector_search", _mock_vector_search, create=True),         patch.object(DocumentQAService, "_call_llm", _mock_call_llm, create=True),         patch.object(DocumentQAService, "answer_hybrid", _mock_answer_hybrid):
        res = client.post(
            "/api/documents/doc-1/qa",
            json={
                "question": "Q?",
                "mode": "hybrid",
                "chat_history": ["Q?"],
            },
        )
        assert res.status_code == 200
        assert res.json() == {
            "answer": "deterministic answer",
            "sources": [
                {"page": 1, "content": "Clause A"},
                {"page": 2, "content": "Clause B"},
            ],
        }
