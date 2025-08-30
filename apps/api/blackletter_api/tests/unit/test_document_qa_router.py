from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.database import SessionLocal
from blackletter_api.models.entities import DocumentChunk

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

    # Verify sample chunk seeded for QA
    with SessionLocal() as session:
        chunk = session.query(DocumentChunk).filter_by(document_id="doc-1").first()
        assert chunk is not None
