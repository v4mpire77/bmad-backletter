# Blackletter — Gap Closure Pack (Agents Complete v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Purpose**: Close all gaps flagged between **Mary → PO → SM** and furnish missing artifacts/story packets so Dev & QA can proceed without ambiguity.  
**Owners**: SM (Sam), Analyst (Mary), PO (Sarah), Architect (Winston), UX (Sally)  
**Date**: 2025‑08‑26

---

## 0) Index
- A. **Scrum Master Story Pack — Missing Stories (full packets)**  
- B. **Rulepack `art28_v1.yaml` — complete detectors (a)–(h)**  
- C. **Weak‑Language Lexicon `weak_language.yaml`**  
- D. **Rulepack Schema Validation (JSON Schema + Pydantic)**  
- E. **Gold Set v1 & Scorer CLI**  
- F. **Sharding Execution Plan & Expected Tree**  
- G. **Authoritative `core-config.yaml`**  
- H. **Error Codes & Microcopy**  
- I. **PII Redaction Module (if LLM enabled)**  
- J. **Windows Run Scripts (`ps1`)**  
- K. **Minimal CI (GitHub Actions)**  
- L. **Brand/Export Assets & Legal Copy**  
- M. **QA Scaffolds & Checklists**  
- N. **Dev Onboarding — First 30 minutes**

---

## A) Scrum Master Story Pack — Missing Stories (full packets)

### Story 1.3 — Evidence Window Builder (±2 sentences)
**ID**: 1.3  
**Epic**: 1 — Ingestion & Extraction  
**Status**: **Approved**  
**Goal**: Given a char span in extracted text, return a window of **±N sentences** (default 2) with page/offsets, respecting page boundaries.

**Acceptance Criteria**
1) Function `build_window(analysis_id, start, end, n_sentences=2)` returns `{ snippet, page, start, end }`.  
2) Uses persisted **sentence index** and **page map** from 1.2; never crosses document bounds.  
3) Handles spans inside a sentence, across sentences, and near beginning/end of doc.  
4) Optional debug endpoint `GET /api/analyses/{id}/window?start=..&end=..&n=..` returns preview (dev only).  
5) Unit tests cover boundary cases + non‑ASCII; perf sufficient to support p95 ≤ 60s E2E.

**Backend Tasks**
- `services/evidence.py`: implement `build_window` + helpers.  
- Add router (dev‑only) under `routers/devtools.py` (guarded by env flag).

**Tests**
- Synthetic texts; boundary cases; page boundary case; multibyte characters.

**Artifacts**
- `services/evidence.py`, `routers/devtools.py`, unit tests.

---

### Story 2.4 — Token Ledger & Caps
**ID**: 2.4  
**Epic**: 2 — Rule Engine & Detection  
**Status**: **Approved**  
**Goal**: Track tokens per analysis (even if LLM disabled → zero), enforce hard cap, and flag over‑budget cases as `needs_review`.

**Acceptance Criteria**
1) `tokens_per_doc` recorded in `Metric` for every analysis; `llm_invoked` boolean.  
2) `hard_cap_tokens_per_doc` from `core-config.yaml` enforced; on exceed → detection stops, findings set to `needs_review` where incomplete; error recorded as `reason: 'token_cap'`.  
3) Admin metrics page displays **tokens/doc** and **%docs_invoking_LLM**.  
4) Unit tests simulate ledger increments and cap breach.

**Backend Tasks**
- `services/llm_gate.py` (adapter with counters); integrate into detection path.  
- Update `models/entities.py (Metric)` and `services/metrics.py`.

**Frontend Tasks**
- Metrics tiles reflect new fields.

**Artifacts**
- `services/llm_gate.py`, updates to metrics, tests.

---

### Story 3.2 — Report Export (PDF/HTML)
**ID**: 3.2  
**Epic**: 3 — Findings & Report UI  
**Status**: **Approved**  
**Goal**: Export findings to PDF/HTML with headings, snippets, timestamps, and branding.

**Acceptance Criteria**
1) `POST /api/reports/{analysis_id}` builds HTML from a server template and renders **PDF** using headless Chromium; returns `{ url }`.  
2) HTML export available as fallback (`.html`).  
3) Export includes file metadata (name, checksum, created_at), verdict summary chips, per‑detector cards with **snippet** + **rule id** + **page/offsets**, and **legal disclaimers** (see Section L).  
4) Snapshot test compares generated PDF text layer against golden sample.  
5) PDF size < 3MB for baseline doc.

**Backend Tasks**
- `services/reporting.py` → build HTML; Chromium print‑to‑PDF; persistence to artefacts dir.  
- `routers/reports.py` endpoint.

**Frontend Tasks**
- `ExportDialog` (options: include logo, metadata, date format); button in Findings header.

**Artifacts**
- `services/reporting.py`, `routers/reports.py`, `web/components/ExportDialog.tsx`, snapshots.

---

### Story 4.1 — Metrics Wall (Admin)
**ID**: 4.1  
**Epic**: 4 — Metrics & Observability  
**Status**: **Approved**  
**Goal**: Display key metrics tiles and sparkline trends for admin.

**Acceptance Criteria**
1) Tiles: **p95 latency**, **tokens/doc**, **%LLM usage**, **explainability rate**.  
2) Endpoint `/api/admin/metrics` returns aggregates over last 30 runs + time series.  
3) Sparkline chart per metric (lazy‑loaded); AA contrast; accessible labels.  
4) Unit test aggregates; UI test renders tiles with data.

**Artifacts**
- API: `routers/admin.py`, `services/metrics.py` (aggregations).  
- UI: `web/app/admin/metrics/page.tsx`, `web/components/MetricTile.tsx`.

---

### Story 4.2 — Coverage Meter
**ID**: 4.2  
**Epic**: 4 — Metrics & Observability  
**Status**: **Approved**  
**Goal**: Visualize detector coverage and warn on unknown/missing topics.

**Acceptance Criteria**
1) Compute coverage per analysis: all eight detectors present with a verdict.  
2) Expose in `/api/analyses/{id}` a `coverage: { present: 8, total: 8 }` field.  
3) UI shows bar/progress with warning state if `< total`.  
4) Tests for correct computation.

**Artifacts**
- API and UI updates; unit tests.

---

### Story 5.1 — Org Settings (LLM/OCR/Retention)
**ID**: 5.1  
**Epic**: 5 — Governance & Settings  
**Status**: **Approved**  
**Goal**: Admin can view/edit organization settings that influence privacy/cost.

**Acceptance Criteria**
1) Settings fields: `llm_provider (none|openai|anthropic|gemini)`, `ocr_enabled (bool)`, `retention_policy ('none'|'30d'|'90d')`.  
2) Defaults: `none`, `false`, `'none'`.  
3) REST: `GET/PUT /api/settings/org` (Admin only).  
4) UI: `/settings` page with form; shows **privacy note** and **cost note**; changes audited.

**Artifacts**
- `models/entities.py (OrgSetting)`, `routers/settings.py`, `web/app/settings/page.tsx`.

---

### Story 5.2 — Minimal Auth & Roles (Admin/Reviewer)
**ID**: 5.2  
**Epic**: 5 — Governance & Settings  
**Status**: **Approved**  
**Goal**: Provide minimal role‑based access control.

**Acceptance Criteria**
1) Session cookie auth; `User(id, email, role in {admin, reviewer})`.  
2) Admin can access `/settings` and `/admin/*`; Reviewer cannot.  
3) Upload/Export available to both.  
4) CSRF protection for state‑changing endpoints; secure flags in cookies.

**Artifacts**
- `models/entities.py (User)`, middleware/auth utils, route guards, minimal login form (dev: magic link or local seed).

---

## B) Rulepack `art28_v1.yaml` — Complete Detectors (a)–(h)
> **Note**: Patterns are for detection and *not legal advice*. Anchors/hedges keep recall high and false greens low. Edit to suit corpus.

```yaml
meta:
  pack_id: art28_v1
  evidence_window_sentences: 2
  verdicts: [pass, weak, missing, needs_review]
  tokenizer: sentence

shared_lexicon:
  hedges:
    - commercially reasonable
    - reasonable efforts
    - industry standard
    - where practicable
    - where feasible
    - endeavour
    - as appropriate
    - periodically
    - to the extent possible
  discretion:
    - may
    - at our discretion
    - subject to provider policies
    - if we deem necessary

# (a) Controller instructions only
Detectors:
  - id: A28_3_a_instructions
    anchors_any:
      - only on documented instructions
      - only on written instructions
      - process .* only on .* instructions
    allow_carveouts:
      - unless required by (Union|Member State) law
    weak_nearby: { any: "@hedges" }
    redflags_any:
      - subject to provider policies
      - at (our|its) discretion .* process personal data

  # (b) Confidentiality of authorised persons
  - id: A28_3_b_confidentiality
    anchors_all:
      - persons authorised
      - confidentiality
    weak_nearby: { any: "@hedges" }
    redflags_any:
      - where feasible
      - business purposes

  # (c) Security measures (Art. 32)
  - id: A28_3_c_security
    anchors_any:
      - technical and organisational measures
      - Article 32
    weak_nearby: { any: [commercially reasonable security, industry standard] }
    redflags_any:
      - subject to change without notice

  # (d) Sub‑processors & flow‑down
  - id: A28_3_d_subprocessors
    anchors_any:
      - prior authorisation of sub-processor
      - prior authorisation of subprocessor
      - maintain a list of sub-processors
      - prior notice .* appointment of sub-processors
    flowdown_any:
      - obligations .* equivalent
      - obligations .* no less protective
      - flow-down .* obligations
    weak_nearby: { any: [materially similar, substantially equivalent] }
    redflags_any:
      - unrestricted appointment of sub-processors
      - notice only after onboarding

  # (e) Assistance with data subject rights (Arts. 12–23)
  - id: A28_3_e_dsar_assist
    anchors_any:
      - assist the controller .* (Articles|Arts\.)? ?12-23
      - assist the controller .* requests of data subjects
      - assist .* obligations .* data subject rights
    weak_nearby: { any: "@hedges" }
    redflags_any:
      - assistance .* at (our|its) sole discretion
      - assistance .* subject to separate consulting fees

  # (f) Personal data breach notification without undue delay
  - id: A28_3_f_breach_notice
    anchors_any:
      - notify .* without undue delay .* personal data breach
      - notify the controller without undue delay
    weak_nearby: { any: [as soon as practicable, within a reasonable time] }
    redflags_any:
      - notify .* only if .* internal threshold
      - no timing commitment

  # (g) Return or deletion at end of services (incl. copies)
  - id: A28_3_g_return_delete
    anchors_any:
      - at the end of the provision .* delete or return personal data
      - delete or return .* at end of services
    copies_any:
      - delete copies
      - erase copies
    weak_nearby: { any: [periodically delete] }
    redflags_any:
      - retain .* for analytics by default
      - delete only upon request (no default)

  # (h) Information availability & audits
  - id: A28_3_h_audits_info
    anchors_all:
      - make available all information
      - demonstrate compliance
    audits_any:
      - allow for and contribute to audits
      - including inspections
    weak_nearby: { any: [subject to provider policies, attestations only] }
    redflags_any:
      - audits disallowed
      - SOC2 only regardless of scope
```

---

## C) Weak‑Language Lexicon `weak_language.yaml`
```yaml
lexicon_id: weak_language_v0
hedges:
  - commercially reasonable
  - reasonable efforts
  - industry standard
  - where practicable
  - where feasible
  - endeavour
  - as appropriate
  - periodically
  - to the extent possible
discretion:
  - may
  - at our discretion
  - subject to provider policies
  - if we deem necessary
ambiguity:
  - materially similar
  - substantially equivalent
  - generally consistent
vagueness_time:
  - as soon as practicable
  - within a reasonable time
```

---

## D) Rulepack Schema Validation

### JSON Schema (YAML expressed as JSON Schema for validation)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Art28 Rulepack",
  "type": "object",
  "required": ["meta", "shared_lexicon", "Detectors"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["pack_id", "evidence_window_sentences", "verdicts"],
      "properties": {
        "pack_id": {"type": "string"},
        "evidence_window_sentences": {"type": "integer", "minimum": 1},
        "verdicts": {"type": "array", "items": {"enum": ["pass", "weak", "missing", "needs_review"]}}
      }
    },
    "shared_lexicon": {"type": "object"},
    "Detectors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id"],
        "properties": {
          "id": {"type": "string"},
          "anchors_any": {"type": "array", "items": {"type": "string"}},
          "anchors_all": {"type": "array", "items": {"type": "string"}},
          "allow_carveouts": {"type": "array", "items": {"type": "string"}},
          "weak_nearby": {"type": "object"},
          "redflags_any": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

### Pydantic Model (Python)
```python
class WeakNearby(BaseModel):
    any: list[str] | None = None
    all: list[str] | None = None

class Detector(BaseModel):
    id: str
    anchors_any: list[str] | None = None
    anchors_all: list[str] | None = None
    allow_carveouts: list[str] | None = None
    weak_nearby: WeakNearby | None = None
    redflags_any: list[str] | None = None

class Meta(BaseModel):
    pack_id: str
    evidence_window_sentences: int = Field(ge=1)
    verdicts: list[Literal['pass','weak','missing','needs_review']]

class Rulepack(BaseModel):
    meta: Meta
    shared_lexicon: dict[str, Any]
    Detectors: list[Detector]
```

---

## E) Gold Set v1 & Scorer CLI

**Corpus**: 12–20 contracts (public or synthetic), each labeled for detectors (a)–(h).  
**Label** (JSONL per finding):
```json
{"doc_id":"acme_dpa_001","detector":"A28_3_a_instructions","verdict":"pass","span":{"page":7,"start":1423,"end":1562},"rationale":"anchor present"}
```

**Scorer CLI (`tools/score_goldset.py`)**
```python
# usage: py tools/score_goldset.py --pred preds.jsonl --gold gold.jsonl
# prints per-detector P/R and macro averages + p95 latency + tokens/doc
```
**Output**
```
A28_3_a: P=0.88 R=0.92 | A28_3_b: P=0.86 R=0.90 | ...
Macro: P=0.87 R=0.91 | p95_latency=48s | tokens/doc=0 | %LLM=0%
```

**Fixtures**: at least 3 **positive** and 3 **hard negative** snippets per detector.

---

## F) Sharding Execution Plan & Expected Tree

**Commands** (choose one):
- BMAD: `*shard-doc docs/prd.md prd` ; `*shard-doc docs/architecture.md architecture`  
- CLI: `md-tree explode docs/prd.md docs/prd` ; `md-tree explode docs/architecture.md docs/architecture`

**Expected tree**
```
docs/
  prd.md
  architecture.md
  prd/
    epic-1.md
    epic-2.md
    ...
  architecture/
    tech_stack.md
    coding_standards.md
    source_tree.md
    api_contracts.md
  stories/
    story-1.1.md
    story-1.2.md
    story-1.3.md
    story-2.1.md
    ...
```

**Post‑shard**: update `dev_load_always_files` to include architecture shards.

---

## G) Authoritative `core-config.yaml`
```yaml
llm:
  provider: none           # none|openai|anthropic|gemini
  gate_policy: snippet_only
  snippet_max_tokens: 220
budget:
  hard_cap_tokens_per_doc: 1500
  on_exceed: needs_review
cache:
  kind: sqlite
  key: [prompt_id, snippet_hash]
ocr:
  enabled: false
security:
  redact_pii: true         # if LLM enabled, apply redaction first
```

---

## H) Error Codes & Microcopy

| Code | Message | Hint / UX Copy |
|---|---|---|
| file_too_large | File too large (max 10MB). | Try compressing or split into parts. |
| mime_unsupported | Unsupported file type. | Upload PDF or DOCX. |
| extract_failed | Couldn’t extract text. | File may be image‑only; enable OCR in Settings. |
| token_cap | Token budget exceeded. | Some checks marked *Needs review*. Reduce snippet size or raise cap. |
| report_failed | Couldn’t generate report. | Try again; if persists, download HTML export. |

Legal privacy copy appears on upload page and export footer (see Section L).

---

## I) PII Redaction Module (if LLM enabled)

**Goal**: Redact common PII patterns in snippets before sending to external LLMs.  
**Patterns** (examples; tune as needed):
- Emails: `/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/` → `«email»`  
- Phones: `/\+?[0-9][0-9\-() ]{7,}[0-9]/` → `«phone»`  
- IDs (generic): `/\b[A-Z0-9]{8,}\b/` → `«id»`  
- Addresses (heuristic): common street suffixes → `«address»`

**Acceptance**: unit tests prove masking occurs; original stored server‑side only.

---

## J) Windows Run Scripts (`scripts/ps`)

**dev.ps1**
```powershell
# Run API and Web concurrently (requires two terminals or Start-Process)
$root = Split-Path $MyInvocation.MyCommand.Path -Parent
cd $root\..\..
# API
Start-Process powershell -ArgumentList "-NoExit","-Command","py -3.11 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r apps\api\requirements.txt; $env:CORE_CONFIG_PATH='$(Get-Location)\core-config.yaml'; uvicorn blackletter_api.main:app --app-dir apps\api --reload --host 127.0.0.1 --port 8000"
# Web
Start-Process powershell -ArgumentList "-NoExit","-Command","cd apps\web; npm ci; npm run dev"
```

**test.ps1**
```powershell
# Backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pytest -q apps\api
# Frontend
cd apps\web
npm test -- --run
npx playwright install --with-deps
npx playwright test
```

**lint.ps1**
```powershell
# Python
ruff apps\api --fix
black apps\api
# Web
cd apps\web
npm run lint
npm run format
```

---

## K) Minimal CI (GitHub Actions)

**.github/workflows/backend.yml**
```yaml
name: backend
on: [push, pull_request]
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r apps/api/requirements.txt
      - run: pytest -q apps/api
```

**.github/workflows/frontend.yml**
```yaml
name: frontend
on: [push, pull_request]
jobs:
  web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd apps/web && npm ci && npm run build && npm test -- --run
```

---

## L) Brand/Export Assets & Legal Copy

**Assets**
- `web/public/brand/logo.svg` (placeholder)  
- Export header template includes logo, product name, file name, checksum, timestamp.

**Legal copy**
- UI footer + export footer:  
  *“Blackletter provides automated checks against selected GDPR processor obligations. Results are for information only and **do not constitute legal advice**. Always consult a qualified professional.”*  
- Privacy note near upload:  
  *“Your file stays private. LLM is **off by default**. When enabled, only short snippets are sent.”*

---

## M) QA Scaffolds & Checklists

**Per‑story checklists** aligned to acceptance criteria for 1.1, 1.2, 1.3, 2.1, 2.2, 2.4, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2.  
**Fixture plan**: `ok_basic.pdf`, `hard_negative.pdf`, `docx_basic.docx`, `image_only.pdf`.  
**Golden outputs**: export PDF text layer snapshot, detector runner JSON sample.

---

## N) Dev Onboarding — First 30 Minutes
1) **Clone & run**: `scripts/ps/dev.ps1` (Windows).  
2) **Seed config**: confirm `core-config.yaml` present (Section G).  
3) **Run tests**: `scripts/ps/test.ps1` — fix any red tests.  
4) **Implement order**: 1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 3.1 → 3.2 → 2.4 → 4.1 → 4.2 → 5.1 → 5.2.  
5) **PR template**: link story id, acceptance criteria, screenshots; update `CHANGELOG.md`.

---

**This pack closes all previously flagged gaps.** Shard docs next, then hand packets to Dev in separate chats per story.

