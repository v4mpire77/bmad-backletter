import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import text

from blackletter_api import database
from blackletter_api.models.schemas import QAResponse, QASource
from blackletter_api.routers import document_qa as document_qa_router
from blackletter_api.services import document_qa as document_qa_service

app = FastAPI()
app.include_router(document_qa_router.router, prefix="/api")
client = TestClient(app)


@pytest.fixture(autouse=True)
def seed_document_chunks():
    engine = database.engine
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS document_chunks"))
        conn.execute(
            text(
                """
                CREATE TABLE document_chunks (
                    document_id TEXT,
                    chunk TEXT
                )
                """
            )
        )
        conn.execute(
            text(
                "INSERT INTO document_chunks (document_id, chunk) VALUES ('doc-1', 'sample chunk')"
            )
        )
    yield
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE document_chunks"))


@pytest.fixture(autouse=True)
def mock_qa_service(monkeypatch):
    async def simple(self, document_id: str, question: str) -> QAResponse:
        if document_id != "doc-1":
            raise HTTPException(status_code=404, detail="Document not found")
        return QAResponse(answer="simple", sources=[])

    async def citations(self, document_id: str, question: str) -> QAResponse:
        if document_id != "doc-1":
            raise HTTPException(status_code=404, detail="Document not found")
        source = QASource(page=1, content="sample chunk")
        return QAResponse(answer="citations", sources=[source])

    async def conversational(
        self, document_id: str, question: str, chat_history=None
    ) -> QAResponse:
        if document_id != "doc-1":
            raise HTTPException(status_code=404, detail="Document not found")
        return QAResponse(answer="conversational", sources=[])

    async def hybrid(
        self, document_id: str, question: str, chat_history=None
    ) -> QAResponse:
        if document_id != "doc-1":
            raise HTTPException(status_code=404, detail="Document not found")
        return QAResponse(answer="hybrid", sources=[])

    monkeypatch.setattr(document_qa_service.DocumentQAService, "answer_simple", simple)
    monkeypatch.setattr(
        document_qa_service.DocumentQAService, "answer_with_citations", citations
    )
    monkeypatch.setattr(
        document_qa_service.DocumentQAService, "answer_with_history", conversational
    )
    monkeypatch.setattr(
        document_qa_service.DocumentQAService, "answer_hybrid", hybrid
    )


@pytest.mark.parametrize(
    "mode,expected_answer,expected_sources",
    [
        (None, "simple", []),
        ("citations", "citations", [{"page": 1, "content": "sample chunk"}]),
        ("conversational", "conversational", []),
        ("hybrid", "hybrid", []),
    ],
)
def test_qa_versions(mode, expected_answer, expected_sources):
    payload = {"question": "What?"}
    if mode:
        payload["mode"] = mode
    res = client.post("/api/documents/doc-1/qa", json=payload)
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["answer"] == expected_answer
    assert data["sources"] == expected_sources


def test_qa_invalid_document_id():
    res = client.post("/api/documents/unknown/qa", json={"question": "What?"})
    assert res.status_code == 404
