# Blackletter — Scrum Master Story Pack (SM v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Owner (Scrum Master)**: Sam  
**Date**: 2025-08-29  
**Intended Readers**: Dev, QA, PM, PO, Architect, UX

> Purpose: Convert approved PRD stories into **developer‑ready packets** with full context, clear acceptance criteria, test data, interfaces, and done‑ness. These packets assume the Architecture (Winston v1), UI/UX (Sally v1), PRD (PM v1), and PO Validation (Sarah v1) as source of truth.

---

## Story 2.3 — Weak‑Language Lexicon v0
**ID**: 2.3  
**Epic**: 2 - Ingestion & Extraction
**Status**: **Approved**  
**Goal**: As a detection system, I need to apply a lexicon of weak language terms to findings to potentially downgrade a 'Pass' verdict to 'Weak' if no strong counter-anchors are found.

### Acceptance Criteria
1) The system shall apply a configurable lexicon of terms to the text within an evidence window.
2) A finding's verdict of 'Pass' shall be downgraded to 'Weak' if a weak-language term is found, unless a counter-anchor term is also present in the same window.
3) The weak-language lexicon and counter-anchor terms must be loaded from a configuration file.

### Interfaces
- **Service**: `weak_lexicon.py: apply_downgrade(findings, windows, counter_anchors)`

### Tasks
**Backend**
- Implement a loader for the weak-language lexicon file.
- Implement a post-processing step for findings that downgrades 'Pass' verdicts to 'Weak' based on the lexicon and counter-anchor logic.
- Add a feature toggle `WEAK_LEXICON_ENABLED` and bundle the lexicon via the rulepack loader.

### Tests
- **Unit**:
  - Test that a 'Pass' verdict is downgraded to 'Weak' when a weak-language term is present.
  - Test that a 'Pass' verdict is NOT downgraded if a counter-anchor term is also present.
  - Test that matching is case-insensitive and respects whole-word boundaries.
  - Test that findings remain unchanged when the feature toggle `WEAK_LEXICON_ENABLED` is disabled.

### Artifacts
- **Files**: 
  - `apps/api/blackletter_api/services/weak_lexicon.py`
  - `apps/api/blackletter_api/services/detector_runner.py` (updated)
  - `apps/api/blackletter_api/rules/lexicons/weak_language.yaml`
  - `apps/api/blackletter_api/tests/unit/test_detector_mapping.py`
  - `apps/api/blackletter_api/tests/unit/test_detector_runner.py` (updated)
