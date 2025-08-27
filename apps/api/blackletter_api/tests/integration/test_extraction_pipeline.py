from __future__ import annotations

from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def _make_pdf_bytes(tmp_path: Path) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello. World! This is a test.")
    p = tmp_path / "test.pdf"
    doc.save(str(p))
    return p.read_bytes()


def test_extraction_json_written_for_pdf(tmp_path, monkeypatch):
    monkeypatch.setenv("JOB_SYNC", "1")
    # Use default extraction path inside tasks
    pdf_bytes = _make_pdf_bytes(tmp_path)

    files = {
        "file": ("hello.pdf", BytesIO(pdf_bytes), "application/pdf"),
    }
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    analysis_id = data["analysis_id"]

    # Verify extraction.json exists and has expected keys
    base = Path(".data") / "analyses" / analysis_id
    extraction = base / "extraction.json"
    assert extraction.exists(), f"missing {extraction}"
    payload = __import__("json").loads(extraction.read_text(encoding="utf-8"))
    assert "text_path" in payload
    assert (base / payload["text_path"]).exists()
    assert isinstance(payload.get("page_map"), list) and payload["page_map"], "page_map missing"
    assert isinstance(payload.get("sentences"), list) and payload["sentences"], "sentences missing"
    assert payload.get("meta", {}).get("engine") == "pymupdf"

