from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_list_includes_uploaded_analysis(monkeypatch):
    # Ensure synchronous processing to write analysis.json deterministically
    monkeypatch.setenv("JOB_SYNC", "1")
    # Enable filesystem-backed listing
    monkeypatch.setenv("ANALYSES_FS_ENABLED", "1")

    files = {
        "file": ("doc.pdf", BytesIO(b"%PDF-1.4 minimal"), "application/pdf"),
    }
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201, resp.text
    job = resp.json()
    analysis_id = job["analysis_id"]

    # List analyses and ensure our analysis is present
    res = client.get("/api/analyses?limit=50")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert any(it.get("id") == analysis_id for it in items)
