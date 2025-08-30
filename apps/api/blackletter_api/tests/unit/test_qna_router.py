from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app
import blackletter_api.services.qna_service as qna_service


client = TestClient(app)


def setup_module() -> None:
    text = (
        "Section 1: The contract expires in 2025.\n"
        "Section 2: Acme Corp is liable for damages."
    )
    qna_service.add_document("doc1", text)


def test_document_qna_returns_relevant_chunk() -> None:
    res = client.post(
        "/api/documents/doc1/qa", json={"question": "When does the contract expire?"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"].startswith("Section 1")


def test_document_qna_missing_document() -> None:
    res = client.post(
        "/api/documents/unknown/qa", json={"question": "irrelevant"}
    )
    assert res.status_code == 404

