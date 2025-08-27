from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import fitz  # PyMuPDF
from docx2python import docx2python
from blingfire import text_to_sentences


@dataclass
class PageText:
    page: int
    text: str
    char_start: int
    char_end: int


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


def extract_pdf(path: Path) -> Dict[str, Any]:
    doc = fitz.open(path)
    combined_len = 0
    pages: List[PageText] = []
    all_sentences: List[Dict[str, Any]] = []
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
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
    return {
        "pages": [p.__dict__ for p in pages],
        "sentences": all_sentences,
    }


def extract_docx(path: Path) -> Dict[str, Any]:
    # docx2python flattens content; treat as single page for MVP
    doc = docx2python(str(path))
    # Flatten nested structure into paragraphs joined by double newline
    paras: List[str] = []
    for sec in doc.body:
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


def run_extraction(analysis_id: str, source_file: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = source_file.suffix.lower()
    if suffix == ".pdf":
        result = extract_pdf(source_file)
    elif suffix == ".docx":
        result = extract_docx(source_file)
    else:
        raise ValueError(f"unsupported_file_type: {suffix}")

    # checksum of source file to aid determinism
    h = hashlib.sha256()
    with source_file.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    result["checksum_sha256"] = h.hexdigest()

    out_path = out_dir / "extraction.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f)
    return out_path

