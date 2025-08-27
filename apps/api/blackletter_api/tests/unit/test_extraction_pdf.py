from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from blackletter_api.services.extraction import extract_pdf


def _make_pdf(path: Path, text: str) -> None:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(str(path))
    doc.close()


def test_pdf_extraction_happy(tmp_path):
    pdf = tmp_path / "sample.pdf"
    content = "This is a test. It has two sentences."
    _make_pdf(pdf, content)

    result = extract_pdf(pdf)
    # pages
    assert len(result.pages) == 1
    assert result.pages[0].page == 1
    assert result.pages[0].char_end >= len(result.pages[0].text)
    # sentences
    assert len(result.sentences) >= 2
    # checksum present
    assert len(result.checksum) == 64
