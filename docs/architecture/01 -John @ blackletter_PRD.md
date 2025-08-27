# Blackletter — Product Requirements Document (PRD)

**Project**: Blackletter (GDPR Vendor Contract Checker)

**Owner (PM)**: John  
**Version**: v1.0  
**Date**: 2025‑08‑26  
**Intended Readers**: Analyst (Mary), Architect, PO, SM, Dev, QA

---

## 1) Vision & Goals
**Vision**: Shrink vendor‑contract GDPR review from hours to minutes with **explainable, deterministic checks** against **GDPR Art. 28(3)**, each backed by pinpoint citations and clear rationale.

**Primary Goals (MVP)**
- Deliver **8 obligation checks** from Art. 28(3)(a)–(h) with **Pass / Weak / Missing / Needs review** verdicts.  
- Show **why** for every finding (rule id + snippet + location).  
- **Exportable report** (PDF/HTML) suitable for sharing internally/with vendors.  
- Operate with **low cost** and **tight latency** at small scale.

**Non‑Goals (MVP)**
- Automated redlining or clause rewriting.  
- Multi‑jurisdictional beyond UK/EU GDPR.  
- Batch processing, collaboration, or workflow automation.

---

## 2) Users & Personas
- **DPO / Data Protection Lead** (primary): Needs evidence‑backed clause checks to speed reviews.  
- **In‑house Counsel**: Wants consistent, defensible screening before deep legal work.  
- **External Solicitor**: Quick triage plus an exportable, client‑friendly report.  
- **SME Founder/Ops**: Sanity check on vendor DPAs during procurement.

**Top Jobs‑to‑be‑Done**
1. *Upload a vendor contract* (PDF/DOCX) and receive a **clear, cited** pass/weak/missing summary of the eight Art. 28(3) obligations.  
2. *Drill down* to exact snippets and rule rationales to confirm or challenge a finding.  
3. *Export* a shareable report for stakeholders.

---

## 3) Scope (MVP)
**In‑Scope Functionalities**
1. **File Ingestion**: Upload PDF/DOCX ≤10MB. Async job model with progress.  
2. **Text Extraction & Indexing**: Extract text with **page map + sentence index**; OCR optional (off by default).  
3. **Rule‑Driven Detection**: Run rulepack **art28_v1** across indexed text; compute verdicts per detector.  
4. **Findings UI**: Table/cards with **R/A/G**-style coloring mapped to Pass/Weak/Missing (+ Needs review). Filters, search, and per‑finding detail panel (snippet, rule id, rationale).  
5. **Report Export**: PDF/HTML export with headings, findings, snippets, and metadata.  
6. **History**: Per‑org list of prior analyses with basic metadata (filename, date, verdict summary).  
7. **Settings**: Toggle LLM provider (default **none**), OCR on/off, retention policy, and token budget.

**Out of Scope (MVP)**
- Redline suggestions; vendor compare; cross‑document diffs.  
- Multi‑language contracts; deep PII discovery.  
- SSO & granular RBAC beyond Admin/Reviewer.

---

## 4) Quality Attributes & KPIs
- **Latency**: p95 ≤ 60s end‑to‑end for ≤10MB PDF.  
- **Cost**: ≤ £0.10/document at defaults; token ledger visible per doc.  
- **Accuracy**: Precision ≥ 0.85; Recall ≥ 0.90 on Gold Set v1.  
- **Explainability**: ≥ 95% of findings include snippet + rule id.  
- **Coverage**: No undetected topic among the eight detectors for a compliant DPA.

**Security & Privacy**
- LLM **snippet‑only** gate; provider disabled by default.  
- No PII stored unless retention is explicitly enabled.  
- Signed URLs, server‑side scanning, minimal metadata.

**Accessibility**
- Keyboard navigable; adequate contrast; export readable by screen readers.

---

## 5) Constraints & Assumptions
- **Determinism First**: Regex/lexicon/rules with small, targeted ML only for ambiguity.  
- **Windows‑friendly Dev**; low‑cost infra (Supabase/SQLite/Render/VM acceptable).  
- **Evidence Window**: default ±2 sentences; configurable per detector.  
- **Verdicts**: Pass / Weak / Missing / Needs review (conservative default).

---

## 6) Acceptance Wordings (from Analyst → for Rulepack & QA)
*(Compact view — canonical anchors; full detail in Analyst Pack)*

| Detector | Must‑Include (anchors) | Weak Cues | Red‑Flags |
|---|---|---|---|
| (a) Instructions | only on documented/written instructions; lawful carve‑out notice | commercially reasonable; where practicable; endeavour | provider discretion; subject to provider policies |
| (b) Confidentiality | authorised persons; confidentiality obligation | industry standard; reasonable efforts | where feasible only; business purposes exception |
| (c) Security (Art. 32) | technical and organisational measures; Article 32 | commercially reasonable security; industry standard | subject to change without notice |
| (d) Sub‑processors | prior authorisation/notice; flow‑down equivalence | materially similar; post‑hoc notice | unrestricted appointment; terminate‑only |
| (e) DSAR Assist | assist controller under Arts. 12–23 | reasonable efforts | assistance at sole discretion; paid consulting only |
| (f) Breach Notice | notify without undue delay | as soon as practicable; within a reasonable time | internal threshold required; no timing promise |
| (g) Return/Delete | delete or return at end; delete copies | periodically delete | retain by default for analytics |
| (h) Audits/Info | make available info; allow & contribute to audits | subject to provider policies; attestations‑only | audits disallowed; SOC2‑only regardless of scope |

---

## 7) Epics & Story Map (MVP)

### Epic 1 — Ingestion & Extraction
**Outcome**: Users upload files; service creates text, page map, and sentence index.

- **Story 1.1 — Upload & Job Orchestration** *(draft)*  
  **Acceptance**: POST /contracts accepts PDF/DOCX ≤10MB, returns `job_id`; GET /jobs/{id} yields `queued|running|done|error`. Errors include reason.  
- **Story 1.2 — Text Extraction (PDF/DOCX)** *(draft)*  
  **Acceptance**: For successful jobs, text + page map + sentence index persisted; malformed docs yield graceful error.  
- **Story 1.3 — Evidence Window Builder** *(draft)*  
  **Acceptance**: Given a span (char offsets), returns ±2‑sentence window; configurable per detector.

### Epic 2 — Rule Engine & Detection
**Outcome**: Deterministic checks produce verdicts and evidence.

- **Story 2.1 — Rulepack Loader (art28_v1)** *(draft)*  
  **Acceptance**: Load YAML rulepack; report validation errors; expose detectors list.  
- **Story 2.2 — Detector Runner** *(draft)*  
  **Acceptance**: For each detector, evaluate anchors/weak/red‑flags, compute verdict (see mapping), attach snippet + rule id.  
- **Story 2.3 — Weak‑Language Lexicon v0** *(draft)*  
  **Acceptance**: Lexicon applied within evidence window; downgrades Pass→Weak unless counter‑anchor exists.  
- **Story 2.4 — Token Ledger & Caps** *(draft)*  
  **Acceptance**: Ledger writes tokens_per_doc; hard cap triggers `needs_review`; LLM disabled by default.

### Epic 3 — Findings & Report UI
**Outcome**: Clear, evidence‑first UI and exports.

- **Story 3.1 — Findings Table** *(draft)*  
  **Acceptance**: Shows 8 detectors with verdict color, short rationale, filter by verdict; click opens detail drawer with snippet and rule id.  
- **Story 3.2 — Report Export (PDF/HTML)** *(draft)*  
  **Acceptance**: Export reproduces findings with headings, snippets, timestamps; file name and checksum shown.

### Epic 4 — Metrics & Observability
**Outcome**: Visibility into performance and costs.

- **Story 4.1 — Metrics Wall** *(draft)*  
  **Acceptance**: Capture p95 latency, tokens_per_doc, %docs_invoking_LLM, explainability rate; display on admin metrics page.  
- **Story 4.2 — Coverage Meter** *(draft)*  
  **Acceptance**: Visual shows detector coverage; warns if any detector returns `unknown`.

### Epic 5 — Governance & Settings
**Outcome**: Safe defaults; simple administration.

- **Story 5.1 — Org Settings** *(draft)*  
  **Acceptance**: Toggle LLM provider (none/default), OCR, retention policy; persist securely.  
- **Story 5.2 — Minimal Auth & Roles** *(draft)*  
  **Acceptance**: Admin / Reviewer roles; Admin controls settings; Reviewer can upload and export only.

---

## 8) Detailed Story Templates (for SM → Dev)
> Stories start as **status: draft**. PO will flip to **approved** before Dev.

### Story 1.1 — Upload & Job Orchestration
```
id: 1.1
epic: 1
title: Upload & Job Orchestration
status: draft
acceptance_criteria:
  - POST /contracts accepts PDF/DOCX ≤10MB; returns job_id
  - GET /jobs/{id} returns status: queued|running|done|error (+ error reason)
  - On done, analysis record exists with filename, size, created_at
  - Latency budget: enqueue < 500ms server time
notes:
  - Virus/size checks server‑side; signed upload URL optional
```  

### Story 1.2 — Text Extraction (PDF/DOCX)
```
id: 1.2
epic: 1
title: Text Extraction (PDF/DOCX)
status: draft
acceptance_criteria:
  - Extract text → page map (page→char range) + sentence index
  - Store extraction artefacts linked to analysis record
  - Malformed/corrupt docs handled with explicit error codes
  - OCR default off; config flag enables OCR path
```

### Story 1.3 — Evidence Window Builder
```
id: 1.3
epic: 1
title: Evidence Window Builder (±2 sentences)
status: draft
acceptance_criteria:
  - Given a char span, return ±2 sentences (configurable per detector)
  - Respect sentence boundaries; avoid cross‑page leakage
  - Unit tests with synthetic spans
```

### Story 2.1 — Rulepack Loader (art28_v1)
```
id: 2.1
epic: 2
title: Rulepack Loader (art28_v1)
status: draft
acceptance_criteria:
  - Load YAML; validate schema; list detectors and lexicons
  - On invalid YAML, surface clear errors
  - Config: rules path env var; hot‑reload disabled in prod
```

### Story 2.2 — Detector Runner
```
id: 2.2
epic: 2
title: Detector Runner (verdict + evidence)
status: draft
acceptance_criteria:
  - Evaluate anchors/weak/red‑flags within evidence window
  - Produce verdict per mapping; attach rule id + snippet + offsets
  - Unit tests: 3 positive + 3 hard negative per detector (a)–(c) to start
```

### Story 2.3 — Weak‑Language Lexicon v0
```
id: 2.3
epic: 2
title: Weak‑Language Lexicon v0
status: draft
acceptance_criteria:
  - Apply lexicon inside evidence window
  - Downgrade Pass→Weak unless counter‑anchor present
  - Configurable lexicon file
```

### Story 2.4 — Token Ledger & Caps
```
id: 2.4
epic: 2
title: Token Ledger & Caps
status: draft
acceptance_criteria:
  - Track tokens_per_doc; expose metric
  - Hard cap triggers needs_review; logged with reason
  - LLM provider off by default
```

### Story 3.1 — Findings Table
```
id: 3.1
epic: 3
title: Findings Table (evidence‑first)
status: draft
acceptance_criteria:
  - 8 detector rows with verdict color and short rationale
  - Detail drawer shows snippet + rule id + copy button
  - Filter by verdict; search within snippets
```

### Story 3.2 — Report Export
```
id: 3.2
epic: 3
title: Report Export (PDF/HTML)
status: draft
acceptance_criteria:
  - PDF/HTML export with headings, verdicts, snippets, timestamps
  - Include file metadata (name, checksum)
  - Asset is reproducible from stored artefacts
```

### Story 4.1 — Metrics Wall
```
id: 4.1
epic: 4
title: Metrics Wall (latency, tokens, %LLM, explainability)
status: draft
acceptance_criteria:
  - Capture and display p95 latency, tokens_per_doc, %docs_invoking_LLM
  - Explainability rate (findings with snippet+rule id)
  - Admin‑only page
```

### Story 4.2 — Coverage Meter
```
id: 4.2
epic: 4
title: Coverage Meter
status: draft
acceptance_criteria:
  - Visual shows detector coverage per doc
  - Warning if any detector returns unknown
```

### Story 5.1 — Org Settings
```
id: 5.1
epic: 5
title: Org Settings (LLM/OCR/Retention)
status: draft
acceptance_criteria:
  - Toggle LLM provider (none/default), OCR, retention policy
  - Persist securely; defaults conservative
  - Audit log for settings changes
```

### Story 5.2 — Minimal Auth & Roles
```
id: 5.2
epic: 5
title: Minimal Auth & Roles (Admin/Reviewer)
status: draft
acceptance_criteria:
  - Admin can manage settings; Reviewer can upload/export only
  - Sessions persisted; CSRF protected
```

---

## 9) Definition of Ready / Done
**DoR (for stories)**: Acceptance criteria written; test data identified; UX implications (if any) defined; dependencies listed.

**DoD**: Unit tests pass; acceptance criteria demonstrated; QA review recorded; metrics updated; documentation snippet added.

---

## 10) Dependencies & Risks
- **Extraction variance**: mitigate with robust parser + graceful errors.  
- **Clause phrasing variance**: rulepack + lexicon; later small ML for triage.  
- **Token cost drift**: strict caps + provider off by default.

---

## 11) Release Plan (MVP)
- **Milestone A**: Epics 1–2 stories (1.1–1.3, 2.1–2.2) complete; smoke run on 3 gold docs.  
- **Milestone B**: Basic UI + export (3.1–3.2); metrics (4.1).  
- **Milestone C**: Coverage meter (4.2), settings (5.1), auth (5.2); MVP freeze.

---

## 12) Open Questions (to resolve early)
- Which LLM provider (if any) to expose first when toggled?  
- Preferred PDF engine for export (wkhtmltopdf vs headless Chromium).  
- Storage: start with SQLite or Supabase Postgres for artefacts?

---

## 13) Appendices
- **A. Analyst Pack Reference**: Acceptance wordings, lexicon, rulepack skeleton, gold‑set schema (see Analyst Hand‑Off v1).  
- **B. Story Template**: Included under §8.

