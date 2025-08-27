# Story 1.3 — Evidence Window Builder (Dev Guide)
Status: Approved

Given a char span and page, return ±N sentences around it, bounded and page-safe.

## Summary
Build evidence windows from `extraction.json` sentence indices to support detector evaluation. No cross-page leakage.

## Allowed Repo Surface
- apps/api/blackletter_api/services/evidence.py
- apps/api/blackletter_api/tests/unit/test_evidence_windows.py (exists)

## Implementation Steps
- Input: page number, start, end, config: before=2, after=2.
- Use sentence indices to find containing sentence(s) and expand by N sentences backward/forward.
- Clamp to page boundaries based on page_map; return `{ page, start, end, text, sentence_indices }`.
- Pure function; no I/O.

## Tests (pytest)
- Window clamps at document and page edges; respects configurable before/after; returns contiguous span; indices monotonic.

