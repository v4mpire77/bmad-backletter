
from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient

from blackletter_api.main import app

client = TestClient(app)


def test_upload_file_too_large():
    """Verify server rejects files > 10MB with 413."""
    # Create a fake file that is just over 10MB
    large_content = b"a" * (10 * 1024 * 1024 + 1)
    files = {
        "file": ("large_doc.pdf", BytesIO(large_content), "application/pdf"),
    }
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 413
    assert resp.json() == {"detail": "file_too_large"}


def test_upload_unsupported_file_type():
    """Verify server rejects non-PDF/DOCX files with 415."""
    files = {
        "file": ("archive.zip", BytesIO(b"zip_content"), "application/zip"),
    }
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 415
    assert resp.json() == {"detail": "unsupported_file_type"}


def test_upload_success_small_pdf():
    """Verify server accepts a valid small PDF."""
    files = {
        "file": ("doc.pdf", BytesIO(b"%PDF-1.4 minimal"), "application/pdf"),
    }
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert "analysis_id" in data
    assert data["status"] == "queued"
