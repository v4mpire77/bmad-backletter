from __future__ import annotations

from pathlib import Path


async def extract_text(path: Path, content_type: str) -> str:
    """Very simple extractor.

    - text/plain: read text (decode errors ignored)
    - application/pdf/doc/docx: return synthetic placeholder text
    """
    if content_type == "text/plain":
        try:
            data = path.read_bytes()
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    if content_type in {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }:
        return "synthetic extracted content"
    return ""

