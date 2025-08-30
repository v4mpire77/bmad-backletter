"""Integration tests for /api/qa/{document_id} route."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from blackletter_api.routers.document_qa import router as qa_router


app = FastAPI()
app.include_router(qa_router, prefix="/api")
client = TestClient(app)


def test_qa_route_simple_mode() -> None:
    """Default QA route should return an answer with no sources."""
    resp = client.post(
        "/api/qa/doc-1",
        json={"question": "What is the purpose?"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer"]
    assert data["sources"] == []


def test_qa_route_citations_mode() -> None:
    """QA route in citation mode should include source details."""
    resp = client.post(
        "/api/qa/doc-1",
        json={"question": "What is the purpose?", "mode": "citations"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer"]
    assert isinstance(data["sources"], list)
    assert data["sources"][0]["page"] == 1

