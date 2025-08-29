# Blackletter — Scrum Master Story Pack (SM v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Owner (Scrum Master)**: Sam  
**Date**: 2025‑08‑26  
**Intended Readers**: Dev, QA, PM, PO, Architect, UX

> Purpose: Convert approved PRD stories into **developer‑ready packets** with full context, clear acceptance criteria, test data, interfaces, and done‑ness. These packets assume the Architecture (Winston v1), UI/UX (Sally v1), PRD (PM v1), and PO Validation (Sarah v1) as source of truth.

---

## Story 1.3 — Evidence Window Builder
**ID**: 1.3  
**Epic**: 1 — Ingestion & Extraction
**Status**: **Approved**  
**Goal**: For a given anchor sentence, construct an ‘evidence window’ of ±N sentences.

### Acceptance Criteria
1) Given a sentence index and an anchor sentence’s index, return a new sentence index for the evidence window.
2) The window size (N) is configurable per detector, with a default of ±2 sentences.
3) The window should not go beyond the bounds of the document (i.e., before the first sentence or after the last sentence).
4) The returned evidence window should be a list of sentences, each with its original index.

### Interfaces
- **Service**: `evidence.py: build_evidence_window(sentence_index, anchor_index, window_size) -> list[tuple[int, str]]`.

### Tasks
**Backend**
- Implement the `build_evidence_window` function in `services/evidence.py`.
- The function should take the full sentence index, the index of the anchor sentence, and the window size as input.
- It should return a list of tuples, where each tuple contains the original sentence index and the sentence text.

### Tests
- **Unit**:
  - Test with an anchor sentence in the middle of the document.
  - Test with an anchor sentence at the beginning of the document.
  - Test with an anchor sentence at the end of the document.
  - Test with a window size of 0.
  - Test with a large window size that exceeds the document boundaries.

### Artifacts
- Files: `services/evidence.py`.
