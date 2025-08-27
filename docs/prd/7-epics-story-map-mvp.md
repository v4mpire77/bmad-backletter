# 7) Epics & Story Map (MVP)

## Epic 1 — Ingestion & Extraction
**Outcome**: Users upload files; service creates text, page map, and sentence index.

- **Story 1.1 — Upload & Job Orchestration** *(draft)*  
  **Acceptance**: POST /contracts accepts PDF/DOCX ≤10MB, returns `job_id`; GET /jobs/{id} yields `queued|running|done|error`. Errors include reason.  
- **Story 1.2 — Text Extraction (PDF/DOCX)** *(draft)*  
  **Acceptance**: For successful jobs, text + page map + sentence index persisted; malformed docs yield graceful error.  
- **Story 1.3 — Evidence Window Builder** *(draft)*  
  **Acceptance**: Given a span (char offsets), returns ±2‑sentence window; configurable per detector.

## Epic 2 — Rule Engine & Detection
**Outcome**: Deterministic checks produce verdicts and evidence.

- **Story 2.1 — Rulepack Loader (art28_v1)** *(draft)*  
  **Acceptance**: Load YAML rulepack; report validation errors; expose detectors list.  
- **Story 2.2 — Detector Runner** *(draft)*  
  **Acceptance**: For each detector, evaluate anchors/weak/red‑flags, compute verdict (see mapping), attach snippet + rule id.  
- **Story 2.3 — Weak‑Language Lexicon v0** *(draft)*  
  **Acceptance**: Lexicon applied within evidence window; downgrades Pass→Weak unless counter‑anchor exists.  
- **Story 2.4 — Token Ledger & Caps** *(draft)*  
  **Acceptance**: Ledger writes tokens_per_doc; hard cap triggers `needs_review`; LLM disabled by default.

## Epic 3 — Findings & Report UI
**Outcome**: Clear, evidence‑first UI and exports.

- **Story 3.1 — Findings Table** *(draft)*  
  **Acceptance**: Shows 8 detectors with verdict color, short rationale, filter by verdict; click opens detail drawer with snippet and rule id.  
- **Story 3.2 — Report Export (PDF/HTML)** *(draft)*  
  **Acceptance**: Export reproduces findings with headings, snippets, timestamps; file name and checksum shown.

## Epic 4 — Metrics & Observability
**Outcome**: Visibility into performance and costs.

- **Story 4.1 — Metrics Wall** *(draft)*  
  **Acceptance**: Capture p95 latency, tokens_per_doc, %docs_invoking_LLM, explainability rate; display on admin metrics page.  
- **Story 4.2 — Coverage Meter** *(draft)*  
  **Acceptance**: Visual shows detector coverage; warns if any detector returns `unknown`.

## Epic 5 — Governance & Settings
**Outcome**: Safe defaults; simple administration.

- **Story 5.1 — Org Settings** *(draft)*  
  **Acceptance**: Toggle LLM provider (none/default), OCR, retention policy; persist securely.  
- **Story 5.2 — Minimal Auth & Roles** *(draft)*  
  **Acceptance**: Admin / Reviewer roles; Admin controls settings; Reviewer can upload and export only.

---
