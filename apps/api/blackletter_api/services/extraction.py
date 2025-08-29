from __future__ import annotations

import json
import os
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

import fitz  # PyMuPDF
from docx2python import docx2python
from blingfire import text_to_sentences

try:  # Optional OCR deps
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
except Exception:  # noqa: BLE001
    pytesseract = None  # type: ignore
    Image = None  # type: ignore

# Configure pytesseract binary path if provided
if pytesseract is not None:
    try:
        _cmd = os.getenv("TESSERACT_CMD")
        if _cmd:
            pytesseract.pytesseract.tesseract_cmd = _cmd  # type: ignore[attr-defined]
    except Exception:
        # Non-fatal: default discovery will be used
        pass


@dataclass
class PageText:
    page: int
    text: str
    char_start: int
    char_end: int

@dataclass
class PdfResult:
    pages: List[PageText]
    sentences: List[Dict[str, Any]]
    checksum: str


class ExtractionError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:  # noqa: D401
        super().__init__(message)
        self.code = code


def _split_sentences_with_offsets(text: str) -> List[Dict[str, Any]]:
    # Use blingfire to split into sentences; then compute offsets by walking text
    # Blingfire may return '\n' separated sentences; we split lines and trim
    raw = text_to_sentences(text)
    sentences = [s.strip() for s in raw.split("\n") if s.strip()]
    items: List[Dict[str, Any]] = []
    pos = 0
    for s in sentences:
        # naive find from current pos
        idx = text.find(s, pos)
        if idx < 0:
            # fallback: skip if cannot locate
            continue
        start = idx
        end = idx + len(s)
        items.append({"start": start, "end": end, "text": s})
        pos = end
    return items


def _page_text_with_optional_ocr(page: "fitz.Page", *, ocr_enabled: bool, ocr_dpi: int, ocr_lang: str, ocr_used_flag: Dict[str, bool]) -> str:
    text = page.get_text("text") or ""
    if text.strip():
        return text
    if not ocr_enabled:
        return text
    if pytesseract is None or Image is None:
        raise ExtractionError("ocr_not_available", "OCR requested but pytesseract/Pillow not available")
    try:
        pm = page.get_pixmap(dpi=ocr_dpi, alpha=False)
        img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
        ocr_text = pytesseract.image_to_string(img, lang=ocr_lang) or ""
        if ocr_text.strip():
            ocr_used_flag["used"] = True
        return ocr_text
    except Exception as exc:  # noqa: BLE001
        raise ExtractionError("ocr_failed", f"OCR failed: {exc}") from exc


def extract_pdf(path: Path) -> PdfResult:
    try:
        doc = fitz.open(path)
    except Exception as exc:  # noqa: BLE001
        raise ExtractionError("pdf_open_failed", f"Failed to open PDF: {exc}") from exc
    combined_len = 0
    pages: List[PageText] = []
    all_sentences: List[Dict[str, Any]] = []
    # OCR toggles via env
    ocr_enabled = os.getenv("OCR_ENABLED", "0") in ("1", "true", "True")
    ocr_dpi = int(os.getenv("OCR_DPI", "200"))
    ocr_lang = os.getenv("TESSERACT_LANG", "eng")
    ocr_used_flag: Dict[str, bool] = {"used": False}
    for i, page in enumerate(doc):
        text = _page_text_with_optional_ocr(
            page,
            ocr_enabled=ocr_enabled,
            ocr_dpi=ocr_dpi,
            ocr_lang=ocr_lang,
            ocr_used_flag=ocr_used_flag,
        )
        start = combined_len
        end = start + len(text)
        pages.append(PageText(page=i + 1, text=text, char_start=start, char_end=end))
        combined_len = end
    # sentences per page with local offsets
    for p in pages:
        for s in _split_sentences_with_offsets(p.text):
            all_sentences.append({
                "page": p.page,
                "start": s["start"],
                "end": s["end"],
                "text": s["text"],
            })
    # checksum of source
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return PdfResult(pages=pages, sentences=all_sentences, checksum=h.hexdigest())


def extract_docx(path: Path) -> Dict[str, Any]:
    # docx2python flattens content; treat as single page for MVP
    try:
        doc = docx2python(str(path))
        # Flatten nested structure into paragraphs joined by double newline
        paras: List[str] = []
        for sec in doc.body:  # May raise on malformed archives
            for row in sec:
                for cell in row:
                    for para in cell:
                        if isinstance(para, str):
                            if para.strip():
                                paras.append(para)
                        elif isinstance(para, list):
                            for item in para:
                                if isinstance(item, str) and item.strip():
                                    paras.append(item)
        text = "\n\n".join(paras)
        pages = [PageText(page=1, text=text, char_start=0, char_end=len(text))]
        sentences = [
            {"page": 1, **s}
            for s in _split_sentences_with_offsets(text)
        ]
        return {
            "pages": [p.__dict__ for p in pages],
            "sentences": sentences,
        }
    except Exception as exc:  # noqa: BLE001
        raise ExtractionError("docx_parse_failed", f"Failed to parse DOCX: {exc}") from exc


def run_extraction(analysis_id: str, source_file: Path, out_dir: Path) -> Path:
    """Extract text and write a normalized extraction.json artifact.

    The JSON schema includes keys compatible with tests:
    - text_path: relative path to extracted text file
    - page_map: list (per-page char spans or metadata)
    - sentences: list of sentence entries with page/start/end/text
    - meta: {engine: str}
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = source_file.suffix.lower()

    text_path = out_dir / "extracted.txt"
    payload: Dict[str, Any] = {
        "analysis_id": analysis_id,
        "source_filename": source_file.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "text_path": text_path.name,
        "page_map": [],
        "sentences": [],
        "meta": {},
    }

    try:
        if suffix == ".pdf":
            pdf_result = extract_pdf(source_file)
            # Write concatenated text from pages
            combined_text = "".join(p.text for p in pdf_result.pages)
            text_path.write_text(combined_text, encoding="utf-8")
            # Build page_map as list of per-page spans
            payload["page_map"] = [
                {"page": p.page, "start": p.char_start, "end": p.char_end}
                for p in pdf_result.pages
            ]
            payload["sentences"] = pdf_result.sentences
            payload["meta"] = {"engine": "pymupdf"}
        elif suffix == ".docx":
            docx_data = extract_docx(source_file)
            combined_text = "".join(p["text"] for p in docx_data.get("pages", []))
            text_path.write_text(combined_text, encoding="utf-8")
            payload["page_map"] = [
                {"page": p["page"], "start": p["char_start"], "end": p["char_end"]}
                for p in docx_data.get("pages", [])
            ]
            payload["sentences"] = docx_data.get("sentences", [])
            payload["meta"] = {"engine": "docx2python"}
        else:
            raise ExtractionError("unsupported_file_type", f"Unsupported file type: {suffix}")
    except ExtractionError as exc:
        # Persist error artifact and re-raise
        try:
            if not text_path.exists():
                text_path.write_text("", encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
        payload["error"] = {"code": exc.code, "message": str(exc)}
        # checksum of source file to aid determinism
        h = hashlib.sha256()
        with source_file.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        payload["checksum_sha256"] = h.hexdigest()
        out_path = out_dir / "extraction.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f)
        raise
    except Exception as exc:  # noqa: BLE001
        # Persist unknown error artifact and re-raise
        try:
            if not text_path.exists():
                text_path.write_text("", encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
        payload["error"] = {"code": "extraction_failed", "message": str(exc)}
        h = hashlib.sha256()
        with source_file.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        payload["checksum_sha256"] = h.hexdigest()
        out_path = out_dir / "extraction.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f)
        raise

    # checksum of source file to aid determinism
    h = hashlib.sha256()
    with source_file.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    payload["checksum_sha256"] = h.hexdigest()

    out_path = out_dir / "extraction.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f)
    return out_path

