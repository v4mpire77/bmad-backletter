# Story 1.2 — Text Extraction (Dev Guide)
Status: Approved

Deterministic extraction from PDF/DOCX into artifacts consumed by detectors.

## Summary
Extract page text and build a sentence index. Persist `extraction.json` under the analysis directory. No OCR/LLM here; explicit errors for corrupt docs.

## Allowed Repo Surface
- apps/api/blackletter_api/services/extraction.py
- apps/api/blackletter_api/services/storage.py (reuse)
- apps/api/blackletter_api/models/schemas.py (optional: artifact model)
- apps/api/blackletter_api/tests/unit/test_extraction_{pdf,docx}.py (already present)

## Implementation Steps
- PDF: use PyMuPDF (fitz) to read text per page, aggregate into a single string; capture page→(start,end) char ranges.
- DOCX: use docx2python (preferred) or python-docx fallback; flatten paragraphs; produce page map with single page if needed.
- Sentence index: use a simple splitter or blingfire; build `[ [start,end], ... ]` indices relative to the aggregated text.
- Persist `.data/analyses/{id}/extraction.json` with: filename, size, created_at, checksum (sha256 of source), pages[], page_map, sentence_indices.
- Errors: raise explicit exceptions for corrupt docs; do not silently pass.

## Tests (pytest)
- Unit: PDF happy; DOCX happy; corrupt doc raises; sentence boundaries non-empty and monotonic; page map spans cover all text ranges.
- Integration: small sample files produce stable JSON shape (keys present; arrays plausible).

## Commands
- `pytest apps/api/blackletter_api/tests -q`

