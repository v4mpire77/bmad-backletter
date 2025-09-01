from fastapi.testclient import TestClient
from backend.main import app
import io

client = TestClient(app)


def test_review_endpoint_accepts_file_and_returns_summary_and_risks(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    # Fake PDF-like bytes; endpoint tolerates non-strict input
    content = b"%PDF-1.4\nThis Agreement covers personal data and liability.\n%%EOF"
    files = {"file": ("test.pdf", io.BytesIO(content), "application/pdf")}
    r = client.post("/api/review", files=files)
    assert r.status_code == 200
    body = r.json()
    assert "summary" in body
    assert "risks" in body
    assert isinstance(body["risks"], list)
