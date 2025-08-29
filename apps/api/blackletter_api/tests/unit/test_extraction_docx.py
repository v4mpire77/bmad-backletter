from __future__ import annotations

from pathlib import Path

import pytest
from docx import Document  # type: ignore

from blackletter_api.services.extraction import extract_docx, ExtractionError


def _make_docx(path: Path, paragraphs: list[str]) -> None:
    doc = Document()
    for p in paragraphs:
        doc.add_paragraph(p)
    doc.save(str(path))


def test_docx_extraction_happy(tmp_path: Path):
    docx_path = tmp_path / "sample.docx"
    _make_docx(docx_path, ["Hello world.", "This is a test document."])

    data = extract_docx(docx_path)
    pages = data.get("pages", [])
    assert len(pages) == 1
    assert pages[0]["page"] == 1
    assert pages[0]["char_end"] >= pages[0]["char_start"]
    sentences = data.get("sentences", [])
    assert len(sentences) >= 2


def test_docx_extraction_malformed(tmp_path: Path):
    # Write an invalid DOCX (not a zip) and expect a structured error
    bad = tmp_path / "bad.docx"
    bad.write_bytes(b"not-a-zip")
    with pytest.raises(ExtractionError) as ei:
        extract_docx(bad)
    assert ei.value.code == "docx_parse_failed"

