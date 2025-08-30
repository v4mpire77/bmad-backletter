from fastapi.testclient import TestClient

from blackletter_api.main import app

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
