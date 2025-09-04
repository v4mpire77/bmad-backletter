from __future__ import annotations

import json
from pathlib import Path

import pytest

from blackletter_api.services.extraction import run_extraction


def test_docx_extraction_happy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    analysis_id = "test-docx"
    out_dir = tmp_path / analysis_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create a dummy .docx file; content won't be parsed due to monkeypatch
    source = out_dir / "sample.docx"
    source.write_bytes(b"dummy-docx-content")

    fake_pages = [
        {"page": 1, "text": "Hello world. This is a docx.", "char_start": 0, "char_end": 31}
    ]
    fake_sentences_local = [
        {"start": 0, "end": 12, "text": "Hello world."},
        {"start": 13, "end": 31, "text": "This is a docx."},
    ]
    fake_sentences = [{"page": 1, **s} for s in fake_sentences_local]

    def fake_extract_docx(path: Path):
        return {"pages": fake_pages, "sentences": fake_sentences}

    monkeypatch.setattr(
        "blackletter_api.services.extraction.extract_docx", fake_extract_docx
    )

    # Act
    extraction_path = run_extraction(analysis_id, source, out_dir)

    # Assert extraction.json integrity
    assert extraction_path.exists(), "extraction.json not created"
    payload = json.loads(extraction_path.read_text(encoding="utf-8"))
    assert payload.get("meta", {}).get("engine") == "docx2python"
    assert isinstance(payload.get("page_map"), list) and payload["page_map"], "page_map missing"
    assert isinstance(payload.get("sentences"), list) and payload["sentences"], "sentences missing"

    # Text file exists and matches combined page text
    text_file = out_dir / payload["text_path"]
    assert text_file.exists(), "extracted text file missing"
    assert text_file.read_text(encoding="utf-8") == "".join(p["text"] for p in fake_pages)

    # sentences.json present and matches
    sentences_json = out_dir / "sentences.json"
    assert sentences_json.exists(), "sentences.json missing"
    sdata = json.loads(sentences_json.read_text(encoding="utf-8"))
    assert sdata.get("sentences") == fake_sentences
    assert sdata.get("page_map")[0]["start"] == fake_pages[0]["char_start"]
    assert sdata.get("page_map")[0]["end"] == fake_pages[0]["char_end"]
