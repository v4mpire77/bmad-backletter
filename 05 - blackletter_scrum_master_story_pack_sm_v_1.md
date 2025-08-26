# Blackletter — Scrum Master Story Pack (SM v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Owner (Scrum Master)**: Sam  
**Date**: 2025‑08‑26  
**Intended Readers**: Dev, QA, PM, PO, Architect, UX

> Purpose: Convert approved PRD stories into **developer‑ready packets** with full context, clear acceptance criteria, test data, interfaces, and done‑ness. These packets assume the Architecture (Winston v1), UI/UX (Sally v1), PRD (PM v1), and PO Validation (Sarah v1) as source of truth.

---

## Global Constraints (apply to all stories)
- **Evidence window**: default ±2 sentences; configurable per detector.  
- **Verdicts**: pass / weak / missing / needs_review; conservative defaults.  
- **LLM**: provider=none by default; snippet‑only if enabled; hard token caps.  
- **Windows‑first**: PowerShell scripts in `scripts/ps/` for run/test/lint.  
- **Dev‑load‑always files**: `docs/architecture/tech_stack.md`, `coding_standards.md`, `source_tree.md`, `core-config.yaml`, `apps/api/.../rules/art28_v1.yaml`, `apps/api/.../rules/lexicons/weak_language.yaml`.

**Shared Types**
```ts
// Finding (generated from Pydantic via OpenAPI/codegen)
export interface Finding {
  detector_id: string;                 // e.g., "A28_3_c_security"
  rule_id: string;                     // e.g., "art28_v1.A28_3_c_security"
  verdict: 'pass'|'weak'|'missing'|'needs_review';
  snippet: string;
  page: number;
  start: number;
  end: number;
  rationale: string;                   // short, user‑readable why
  reviewed: boolean;
}
```

---

## Story 1.1 — Upload & Job Orchestration
**ID**: 1.1  
**Epic**: 1 — Ingestion & Extraction  
**Status**: **Approved**  
**Goal**: Accept PDF/DOCX up to 10MB, create an `analysis` record, enqueue analysis job, and expose job status.

### Acceptance Criteria
1) `POST /api/contracts` accepts multipart `file` (PDF/DOCX ≤10MB) and returns `{ job_id, analysis_id, status: 'queued' }`.  
2) `GET /api/jobs/{job_id}` returns `{ job_id, status: 'queued|running|done|error', error? }`.  
3) On `done`, an `analysis` row exists with `filename`, `size_bytes`, `mime`, `created_at`.  
4) Server rejects oversize/unsupported files with explicit error `{ code, message }`.  
5) Latency budget (enqueue): < 500ms server time.  
6) JSON structured logs include job span and analysis id.

### Interfaces
- **API**: as above.  
- **DB**: `Analysis(id uuid pk, filename, size_bytes, mime, status, created_at, org_id)`.

### Tasks
**Backend**
- Router `uploads.py`: validate MIME/size; save temp file; create `analysis`; enqueue background task; return ids.  
- `services/tasks.py`: `enqueue('analyze', {analysis_id}) -> job_id`; in MVP, uses FastAPI `BackgroundTasks`.  
- `models/entities.py`: SQLAlchemy models for `Analysis`.  
- Logging: add job/analysis correlation ids.

**Frontend**
- `/new` page: drag‑drop uploader → `POST /api/contracts`; then poll `GET /api/jobs/{id}`; show stepper Progress UI.  
- Error banners with precise messages and retry.

### Tests
- **Unit (API)**: size/type validation; happy path returns ids; error model.  
- **Integration**: upload fixture PDF → job status progresses to `done`.  
- **UI (Playwright)**: drag‑drop, progress stepper, error handling.

### Artifacts
- Files: `routers/uploads.py`, `services/tasks.py`, `models/entities.py`, `web/app/new/page.tsx`, `web/components/FileDrop.tsx`.  
- Scripts: `scripts/ps/dev.ps1` (ensure web+api run).

---

## Story 1.2 — Text Extraction (PDF/DOCX)
**ID**: 1.2  
**Epic**: 1 — Ingestion & Extraction  
**Status**: **Approved**  
**Goal**: Convert uploaded document into plain text with page map and sentence index; persist artefacts.

### Acceptance Criteria
1) For a valid PDF/DOCX, produce **text**, **page_map (page→[start,end])**, and **sentence_index** (array of [start,end]).  
2) Persist artefacts under `apps/api/.data/analyses/{analysis_id}/` and link via `ExtractionArtifact`.  
3) Malformed/corrupt files yield error `{ code:'extract_failed', message }` and set job status `error`.  
4) OCR path exists but stays disabled by default; when disabled, fail cleanly on image‑only PDFs with hint.

### Interfaces
- **DB**: `ExtractionArtifact(analysis_id fk, text_path, page_map_path, sentence_idx_path)`.  
- **Service**: `extraction.py: extract(analysis_id, file_path) -> ExtractionResult`.

### Tasks
**Backend**
- PDF via **PyMuPDF**; DOCX via **docx2python**.  
- Build sentence index with **blingfire**; store JSON for `page_map`/`sentence_idx`.  
- Wire into background task: Intake → Extract → (next story triggers detection).

**Frontend**
- Poll job status; on `done`, route to `/analyses/:id`.

### Tests
- **Unit**: sentence splitter correctness (boundaries), page map validity.  
- **Integration**: three fixtures: normal PDF, DOCX, image‑only PDF (expect error when OCR off).  
- **Perf**: extraction must complete to keep end‑to‑end p95 ≤ 60s (baseline doc).

### Artifacts
- Files: `services/extraction.py`, `models/entities.py (ExtractionArtifact)`, test fixtures under `apps/api/tests/fixtures/`.

---

## Story 2.1 — Rulepack Loader (art28_v1)
**ID**: 2.1  
**Epic**: 2 — Rule Engine & Detection  
**Status**: **Approved**  
**Goal**: Load and validate YAML rulepack and expose detectors/lexicons to the runner.

### Acceptance Criteria
1) Load `apps/api/blackletter_api/rules/art28_v1.yaml`; on invalid schema, raise typed error with line/col.  
2) Expose `get_detectors()` and `get_lexicon()` to consumers.  
3) Configurable path via `CORE_CONFIG_PATH` → `core-config.yaml`.  
4) Hot‑reload **disabled** in production; allowed in dev.

### Rulepack Schema (simplified)
```yaml
meta:
  pack_id: string
  evidence_window_sentences: number
  verdicts: [pass, weak, missing, needs_review]
shared_lexicon:
  hedges: string[]
  discretion: string[]
detectors: Det[]

Det:
  id: string
  anchors_any?: string[]
  anchors_all?: string[]
  allow_carveouts?: string[]
  weak_nearby?: { any?: string[]; all?: string[] }
  redflags_any?: string[]
```

### Tasks
**Backend**
- `services/detection.py` → `Rulepack` class with `load_from_yaml(path)` and schema validation.  
- Error types: `RulepackSchemaError`, `RulepackNotFound`.

**Tests**
- Valid rulepack loads; invalid fields produce specific errors; missing file error path.

### Artifacts
- Files: `services/detection.py (Rulepack)`, `rules/art28_v1.yaml` (stub of a–c), `rules/lexicons/weak_language.yaml`.

---

## Story 2.2 — Detector Runner (verdict + evidence)
**ID**: 2.2  
**Epic**: 2 — Rule Engine & Detection  
**Status**: **Approved**  
**Goal**: Evaluate detectors over extracted text using sentence index and produce `Finding[]` with verdicts and snippets.

### Acceptance Criteria
1) For each detector, scan text with `anchors_*`, `weak_nearby`, `redflags_any` within the **evidence window**.  
2) Compute verdict via mapping: Pass (anchor present; no red‑flag) / Weak (anchor + hedge) / Missing (no anchor or contradicted) / Needs review (ambiguous/over budget).  
3) Return `Finding[]` with `rule_id`, `snippet`, `page`, `start`, `end`, `rationale`.  
4) Unit tests include **3 positive + 3 hard negative** for (a)–(c) to start.  
5) Performance: runner on baseline doc completes within the budget to support p95 ≤ 60s.

### Tasks
**Backend**
- Implement windowing via `services/evidence.py`.  
- Implement detector evaluation with regex/keyword families (UTF‑8 safe, case‑insensitive).  
- Verdict mapper function with explicit rules.  
- Compose results and persist `Finding` rows.

**Tests**
- Positive anchors detected; weak cues downgrade; red‑flags override; offsets correctness.

### Artifacts
- Files: `services/evidence.py`, `services/detection.py (DetectorRunner)`, `models/entities.py (Finding)`, `models/schemas.py (Finding schema)`.

---

## Story 3.1 — Findings Table (UI)
**ID**: 3.1  
**Epic**: 3 — Findings & Report UI  
**Status**: **Approved**  
**Goal**: Evidence‑first table presenting eight detectors, verdict chips, rationale, and a right‑side Evidence Drawer.

### Acceptance Criteria
1) Page `/analyses/:id` fetches `GET /api/analyses/{id}` + `GET /api/analyses/{id}/findings`.  
2) Table shows Detector | Verdict chip | short rationale | action (drawer).  
3) Filters: multi‑select by verdict; search across snippets.  
4) Drawer: shows snippet (monospace), highlighted anchors, rule id, page+offsets, copy button; **ESC** closes; focus trapped; ARIA labels on verdict chips.  
5) Contrast meets WCAG AA; color not sole signal (icons + labels).

### Tasks
**Frontend**
- React Query hooks in `web/lib/` for analyses & findings.  
- Components: `FindingsTable`, `VerdictBadge`, `EvidenceDrawer`.  
- CSS tokens per UX spec; responsive layout; keyboard navigation.

**Backend**
- Ensure API payloads match contracts; add pagination if needed (not MVP).  

### Tests
- **UI**: Playwright — filter by verdict; open/close drawer; copy snippet; keyboard nav.  
- **Contract**: Type generation from OpenAPI matches TS usage.

### Artifacts
- Files: `web/app/analyses/[id]/page.tsx`, `web/components/FindingsTable.tsx`, `web/components/EvidenceDrawer.tsx`, `web/components/VerdictBadge.tsx`, hooks in `web/lib/`.

---

## Sprint Plan & Order (recommended)
1) **1.1** Upload & Jobs → **1.2** Extraction → **2.1** Rulepack Loader → **2.2** Detector Runner → **3.1** Findings UI.  
2) Then: **1.3** Evidence Window Builder (if not covered in 2.2), **3.2** Report Export, **4.1** Metrics Wall.

---

## Definition of Done (per story)
- All acceptance criteria met and demoed.  
- Unit & integration tests pass (including fixtures).  
- Lint/format clean; types generated and committed.  
- Logs include ids; metrics recorded where applicable.  
- Minimal docs added to `README.md` or story‑local `docs/`.

---

## Test Fixtures (initial set)
- `fixtures/ok_basic.pdf` — contains clear anchors for (a)–(c).  
- `fixtures/hard_negative.pdf` — look‑alike phrases without anchors.  
- `fixtures/docx_basic.docx` — simple DOCX for pipeline.  
- `fixtures/image_only.pdf` — triggers extract failure when OCR off.

---

## Handoff Notes
- Dev may split stories into subtasks/PRs but must preserve acceptance criteria.  
- QA to write scenario checklists mirroring criteria before coding starts.  
- Any schema or API change must update this pack + Architecture contracts.

