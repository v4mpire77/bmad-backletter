# Blackletter — Product Owner Validation & Approvals (Sarah v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Owner (PO)**: Sarah  
**Date**: 2025‑08‑26  
**Intended Readers**: PM, UX, Architect, SM, Dev, QA

> Purpose: Apply the PO Master Validation Checklist across PRD, UI/UX Spec, and Architecture; resolve gaps; lock decisions; approve initial stories; and prepare documents for sharding.

---

## 0) Executive Summary
- **Problem fit**: Clear and consistently addressed: detect gaps in GDPR Art. 28(3) processor obligations with **explainable** findings (verdict + snippet + rule id).  
- **Scope**: MVP stays tight: 8 detectors (a)–(h), rules‑first, export, basic metrics, safe defaults.  
- **Non‑goals**: Redlining, multilingual, full RAG, collaboration — **explicitly out** of MVP.  
- **KPIs**: p95 ≤ 60s /doc; ≤ £0.10 /doc; Precision ≥ 0.85; Recall ≥ 0.90; Explainability ≥ 95% — feasible within current design.  
- **Decision locks**: LLM **off by default**, snippet‑only if enabled; SQLite dev → Postgres later; BackgroundTasks MVP → Celery later; evidence window ±2 sentences.

**PO Verdict**: ✅ **Green‑light to proceed to Scrum Master** with Story Approvals below.

---

## I. Problem Definition & Context
- **Clarity**: The problem is precisely framed; solution proposes deterministic detectors with grounded citations. **Status: PASS**  
- **Personas & pains**: DPO, in‑house counsel, external solicitor, SME ops — needs addressed via upload→findings→export, evidence‑first UX. **Status: PASS**

**Actions**: none.

---

## II. MVP Scope Definition
- **Scope**: 8 detectors + rulepack `art28_v1`, findings UI, export, basic metrics. **PASS**  
- **Out‑of‑scope**: OCR sophistication, multilingual, redline, batch, collab — **documented**. **PASS**  
- **Performance & cost targets**: documented and testable. **PASS**

**Actions**: none.

---

## III. User Experience Requirements
- **Flows**: Upload → Job status → Findings → Export → History; filters; evidence drawer. **PASS**  
- **Components**: shadcn/ui, verdict chips, table, drawer, progress stepper, toasts. **PASS**  
- **Edge/Loading/Error**: oversized file, corrupt PDF, OCR off, token cap → *Needs review*; clear messages. **PASS**

**Actions**: none.

---

## IV. Functional Requirements
- **Detectors & Rules**: Acceptance wordings and weak‑language lexicon defined; rulepack skeleton provided. **PASS**  
- **LLM integration**: optional, snippet‑only, gated with caps and cache; default none. **PASS**  
- **APIs**: endpoints and schemas are precise (see Freeze §VIII). **PASS**  
- **Data flow**: Intake → Extract → Window → Detect → Report → Metrics. **PASS**

**Actions**: none.

---

## V. Non‑Functional Requirements
- **Performance & scalability**: MVP single‑process async; upgrade path to Celery/Redis; SQLite → Postgres. **PASS**  
- **Security**: data minimization, signed URLs, snippet‑only LLM, settings guardrails. **PASS**  
- **Observability**: metrics captured (latency, tokens, %LLM, explainability); JSON logs. **PASS**

**Actions**: none.

---

## VI. Epics & Story Structure
- **Epics**: Ingestion; Rule Engine; Findings/UI; Metrics; Governance. **PASS**  
- **Stories**: granular, dependency‑aware; acceptance criteria testable. **PASS**

**Actions**: none.

---

## VII. Technical Guidance
- **Standards & versions**: Next.js 14, React 18, TS 5; FastAPI 0.111, Python 3.11, SQLAlchemy 2, Pydantic 2; PyMuPDF/docx2python/blingfire; pins recorded. **PASS**  
- **Shared types**: Pydantic models to TS via OpenAPI/codegen. **PASS**  
- **RAG**: **Not in MVP**; future note only. **PASS**  
- **LLM Judge**: deterministic (temp=0) when enabled; snippet‑only; quote verification; token ledger & caps. **PASS**

**Actions**: none.

---

## VIII. API & Schema Freeze (MVP)

### Endpoints (final for Sprint 1)
- `POST /api/contracts` → create analysis & job → `{ job_id, analysis_id, status }`
- `GET /api/jobs/{job_id}` → job status `{ status, error? }`
- `GET /api/analyses/{analysis_id}` → summary with detector verdicts
- `GET /api/analyses/{analysis_id}/findings` → `Finding[]`
- `POST /api/reports/{analysis_id}` → `{ url }` (PDF/HTML)

### Finding Model (authoritative)
```json
{
  "detector_id": "A28_3_c_security",
  "rule_id": "art28_v1.A28_3_c_security",
  "verdict": "pass|weak|missing|needs_review",
  "snippet": "…technical and organisational measures…",
  "page": 7,
  "start": 1423,
  "end": 1562,
  "rationale": "anchor present; no red‑flag",
  "reviewed": false
}
```

**Error model**: `{ code, message, hint? }`

---

## IX. Risks & Mitigations (PO view)
- **Clause variance** → broad anchors + evidence window; tests + later micro‑classifier.  
- **False reassurance** → conservative defaults; never green without anchor + snippet.  
- **Token drift** → strict caps + provider=none by default; cache.  
- **Extraction variance** → clear errors; user guidance.

---

## X. Decisions Locked (for SM/Dev)
1) **Evidence window**: ±2 sentences (configurable per detector).  
2) **Verdict mapping**: Pass / Weak / Missing / Needs review as defined by rulepack policy.  
3) **LLM**: disabled by default; snippet‑only if enabled; token caps enforced.  
4) **Storage**: SQLite dev; Postgres is not required to start.  
5) **Async**: BackgroundTasks MVP; Celery not required for Sprint 1.

---

## XI. Story Approvals (PO → Approved)
> These stories are approved for Scrum Master packaging and Dev start.

- **Epic 1**  
  - **Story 1.1 — Upload & Job Orchestration** → **Approved**  
  - **Story 1.2 — Text Extraction (PDF/DOCX)** → **Approved**  
  - **Story 1.3 — Evidence Window Builder** → **Approved**

- **Epic 2**  
  - **Story 2.1 — Rulepack Loader (art28_v1)** → **Approved**  
  - **Story 2.2 — Detector Runner (verdict + evidence)** → **Approved**  
  - **Story 2.3 — Weak‑Language Lexicon v0** → **Approved**  
  - **Story 2.4 — Token Ledger & Caps** → **Approved**

- **Epic 3**  
  - **Story 3.1 — Findings Table (evidence‑first)** → **Approved**  
  - **Story 3.2 — Report Export (PDF/HTML)** → **Approved**

- **Epic 4**  
  - **Story 4.1 — Metrics Wall** → **Approved**  
  - **Story 4.2 — Coverage Meter** → **Approved**

- **Epic 5**  
  - **Story 5.1 — Org Settings (LLM/OCR/Retention)** → **Approved**  
  - **Story 5.2 — Minimal Auth & Roles** → **Approved**

**Note**: SM may re‑order within epics for dependency flow (1.1 → 1.2 → 2.1 → 2.2 → 3.1 → 3.2 → 4.1).

---

## XII. Sharding Plan (for PO/SM)

**Goal**: Split large docs into H2‑based shards so agents load only what’s needed.

**Target files**
- `docs/prd.md` → `docs/prd/` (epic list + per‑epic stories)  
- `docs/architecture.md` → `docs/architecture/` (tech_stack.md, coding_standards.md, source_tree.md, api_contracts.md)

**Commands (reference)**
- BMAD task: `*shard-doc docs/prd.md prd`  
- BMAD task: `*shard-doc docs/architecture.md architecture`  
- Optional CLI: `md-tree explode docs/prd.md docs/prd` ; `md-tree explode docs/architecture.md docs/architecture`

**Post‑shard checks**
- Verify epics present and numbered; stories carry `status: draft` until approved.  
- Ensure `dev_load_always_files` include `tech_stack.md`, `coding_standards.md`, `source_tree.md`, `core-config.yaml`, and rulepack files.

---

## XIII. Ready‑for‑SM Handover
- **Input set**: Analyst Hand‑Off Pack v1, PRD v1, UX Spec v1, Architecture v1, this PO Validation v1.  
- **Approved stories**: §XI.  
- **SM tasks**: Create dev‑ready story packets for **1.1, 1.2, 2.1, 2.2, 3.1** (at minimum); auto‑carry architectural context and acceptance criteria; embed test data references.

---

## XIV. Open Questions (non‑blocking)
1) Initial LLM provider to expose in Settings when toggled (OpenAI vs Anthropic vs Gemini).  
2) PDF export engine: headless Chromium (default) vs wkhtmltopdf.  
3) Storage from day‑1: SQLite only vs immediate Postgres.  

*(PO recommends defer: Settings may list provider placeholders; Chromium export; start with SQLite.)*

---

## XV. PO Sign‑off
I confirm the artifacts are cohesive, acceptance criteria are testable, and the architecture supports the MVP. Proceed to **Scrum Master** for story packet drafting and Dev scheduling.
