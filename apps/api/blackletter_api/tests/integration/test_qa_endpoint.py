from fastapi.testclient import TestClient
import pytest

from fastapi import FastAPI

from blackletter_api.models.schemas import QAResponse
from blackletter_api.services.document_qa import DocumentQAService
from blackletter_api.routers import document_qa


app = FastAPI()
app.include_router(document_qa.router, prefix="/api")
client = TestClient(app)


@pytest.fixture
def document_chunks():
    return [
        {"page": 1, "content": "alpha", "score": 0.1},
        {"page": 2, "content": "bravo", "score": 0.9},
        {"page": 3, "content": "charlie", "score": 0.5},
    ]


@pytest.fixture(autouse=True)
def patch_service(document_chunks, monkeypatch):
    service = DocumentQAService()

    async def simple(document_id: str, question: str) -> QAResponse:
        return QAResponse(answer="simple", sources=[])

    async def citations(document_id: str, question: str) -> QAResponse:
        sources = service._extract_sources(document_chunks, top_k=2)
        return QAResponse(answer="citations", sources=sources)

    async def conversational(
        document_id: str, question: str, chat_history=None
    ) -> QAResponse:
        last = chat_history[-1] if chat_history else ""
        return QAResponse(answer=f"conv:{last}", sources=[])

    async def hybrid(
        document_id: str, question: str, chat_history=None
    ) -> QAResponse:
        sources = service._extract_sources(document_chunks, top_k=3)
        return QAResponse(answer="hybrid", sources=sources)

    monkeypatch.setattr(service, "answer_simple", simple)
    monkeypatch.setattr(service, "answer_with_citations", citations)
    monkeypatch.setattr(service, "answer_with_history", conversational)
    monkeypatch.setattr(service, "answer_hybrid", hybrid)
    monkeypatch.setattr(document_qa, "service", service)
    yield


def test_simple_version():
    res = client.post(
        "/api/documents/doc-1/qa",
        json={"question": "What?"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "simple"
    assert data["sources"] == []


def test_citations_version(document_chunks):
    res = client.post(
        "/api/documents/doc-1/qa",
        json={"question": "What?", "mode": "citations"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "citations"
    assert [s["page"] for s in data["sources"]] == [2, 3]


def test_conversational_version():
    res = client.post(
        "/api/documents/doc-1/qa",
        json={
            "question": "What?",
            "mode": "conversational",
            "chat_history": ["hi", "previous"],
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "conv:previous"
    assert data["sources"] == []


def test_hybrid_version(document_chunks):
    res = client.post(
        "/api/documents/doc-1/qa",
        json={"question": "What?", "mode": "hybrid"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "hybrid"
    pages = [s["page"] for s in data["sources"]]
    assert pages == [2, 3, 1]
