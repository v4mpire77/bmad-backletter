# Blackletter — Architecture Specification (v1)

**Project**: Blackletter (GDPR Vendor Contract Checker)  
**Owner (Architect)**: Alex  
**Date**: 2025‑08‑26  
**Intended Readers**: PM, PO, SM, Dev, QA

> Goal: Define a **deterministic, explainable** architecture that turns PRD epics into a production‑ready MVP with Windows‑friendly workflows, low cost, and optional/disabled‑by‑default LLM usage.

---

## 1) Architecture Overview

**Pattern**: Modular services with a thin API, an async‑capable job layer, and a rule‑based detection engine.  
**Data flow**:
1) **Upload** (PDF/DOCX) → `analysis` record + async job id.  
2) **Extract** → plain text, page map, sentence index.  
3) **Detect** → run **art28_v1** rulepack; produce findings with **verdict + snippet + offsets + rule id**.  
4) **Store** → artefacts + findings persisted; metrics recorded.  
5) **Present** → UI tables/cards; evidence drawer; export PDF/HTML.

**Determinism first**: rulepack (YAML) + lexicons; **LLM off** by default; snippet‑only gates if enabled.  
**Evidence window**: default **±2 sentences**; configurable per detector.

---

## 2) Technology Stack (versions locked)

### Frontend
- **Next.js 14** (App Router), **TypeScript 5.x**
- **Tailwind CSS 3.x**, **shadcn/ui**, Radix primitives
- **React Query** for data fetching state
- **PDF export** via headless Chromium (Next.js route) for consistency

### Backend
- **Python 3.11+**, **FastAPI 0.11x**, **Uvicorn**
- Extraction: **PyMuPDF (fitz)** for PDF, **python‑docx/docx2python** for DOCX
- Sentence index: **blingfire** (fast, Windows‑friendly)
- Rules: native regex + YAML rulepack loader
- Optional OCR (off by default): **pytesseract** + Tesseract (Windows install instructions in Appendix A)

### Storage & Infra
- **DB (local dev)**: **SQLite** (simple, file‑backed)
- **DB (cloud)**: **Postgres** (Supabase) — same schema
- **Static/artefacts**: local filesystem in dev; object storage when hosted
- **Async jobs**: **FastAPI BackgroundTasks** for MVP; upgrade path: **Celery + Redis**

### Tooling & QA
- **Pytest** + **pytest‑asyncio** for backend tests
- **Vitest/Playwright** for frontend
- **Ruff/Black** (Python) and **ESLint/Prettier** (TS) for standards

---

## 3) Source Tree (proposed)

```
blackletter/
  apps/
    web/                     # Next.js 14 app
      app/
      components/
      lib/
      styles/
      public/
      package.json
      tsconfig.json
    api/                     # FastAPI service
      blackletter_api/
        main.py
        config.py            # env & core-config.yaml loader
        routers/
          uploads.py
          jobs.py
          analyses.py
          reports.py
        services/
          extraction.py      # PDF/DOCX → text, page map, sentence index
          evidence.py        # ±2 sentence windows
          detection.py       # rulepack runner, verdict mapping
          metrics.py
        rules/
          art28_v1.yaml
          lexicons/
            weak_language.yaml
        models/
          db.py              # SQLAlchemy engine/session
          schemas.py         # Pydantic I/O models
          entities.py        # ORM models
        tests/
          unit/
          integration/
      pyproject.toml
      requirements.txt
  docs/
    prd.md
    architecture.md
    prd/
    architecture/
    stories/
  core-config.yaml           # dev_load_always_files, LLM gate, caps
  README.md
```

---

## 4) Coding Standards (extract)

### Python
- **Ruff/Black** enforced; **pydantic v2** for request/response models.
- Use **async** endpoints when I/O bound; prefer explicit types.
- Business logic sits in `services/`, not in routers.

### TypeScript/React
- **Functional components**, server actions where appropriate.
- **React Query** for API calls; custom hooks in `web/lib/`.
- **UI**: evidence‑first; avoid heavy global state.

---

## 5) Domain Model & Storage

### Entities
- **Analysis**: `id (uuid)`, `filename`, `size_bytes`, `mime`, `status`, `created_at`, `org_id (nullable)`
- **ExtractionArtifact**: `analysis_id (fk)`, `text_path`, `page_map_path (json)`, `sentence_idx_path (json)`
- **Finding**: `id`, `analysis_id (fk)`, `detector_id`, `verdict`, `rule_id`, `snippet`, `page`, `start`, `end`, `rationale`, `created_at`
- **Metric**: `analysis_id`, `latency_ms`, `tokens_used`, `llm_invoked (bool)`, `explainability_hit (bool)`
- **OrgSetting**: `org_id`, `llm_provider`, `ocr_enabled`, `retention_policy`, `created_at`

### Notes
- In dev, artefacts live under `apps/api/.data/analyses/{analysis_id}/...`  
- In cloud, artefacts move to object storage; DB stores pointers only.

---

## 6) API Design (contract‑first)

Base URL examples (dev):
- API: `http://localhost:8000`
- Web: `http://localhost:3000`

### POST /contracts  — Upload & create job
**Request**: multipart form (file: PDF/DOCX; ≤10MB)  
**Response 201**:
```json
{ "job_id": "uuid", "analysis_id": "uuid", "status": "queued" }
```
**Errors**: 400 (type/size), 415 (unsupported)

### GET /jobs/{id}
**Response 200**:
```json
{ "job_id": "uuid", "status": "queued|running|done|error", "error": null }
```

### GET /analyses/{id}
**Response 200** (summary):
```json
{
  "analysis_id": "uuid",
  "filename": "dpa.pdf",
  "created_at": "2025-08-26T19:12:00Z",
  "verdicts": [
    {"detector_id":"A28_3_a_instructions","verdict":"pass"},
    {"detector_id":"A28_3_b_confidentiality","verdict":"weak"}
  ]
}
```

### GET /analyses/{id}/findings
**Response 200** (detailed findings):
```json
[{
  "detector_id": "A28_3_a_instructions",
  "rule_id": "art28_v1.A28_3_a_instructions",
  "verdict": "pass",
  "snippet": "Processor shall process personal data only on documented instructions of the Controller…",
  "page": 7, "start": 1423, "end": 1562,
  "rationale": "anchor present; no red‑flag"
}]
```

### POST /reports/{analysis_id}
**Response 201**: `{ "url": "/api/reports/{file}.pdf" }`

---

## 7) Detection Engine (rule‑first)

### Rulepack schema (simplified)
```yaml
meta:
  pack_id: art28_v1
  evidence_window_sentences: 2
  verdicts: [pass, weak, missing, needs_review]
shared_lexicon:
  hedges: ["commercially reasonable", "reasonable efforts", "industry standard", "where practicable", "endeavour", "as appropriate", "periodically", "to the extent possible"]

# Detector (a)
detectors:
  - id: A28_3_a_instructions
    anchors_any:
      - "only on documented instructions"
      - "only on written instructions"
      - "process .* only on .* instructions"
    allow_carveouts:
      - "unless required by (Union|Member State) law"
    weak_nearby: { any: "@hedges" }
    redflags_any:
      - "subject to provider policies"
      - "at (our|its) discretion .* process personal data"

# … repeat (b)–(h)
```

### Verdict mapping
- **Pass**: must‑include anchor present; no red‑flag.  
- **Weak**: anchor present but a weak cue in window without counter‑anchor.  
- **Missing**: anchor absent or contradicted by a red‑flag.  
- **Needs_review**: ambiguous/over budget.

---

## 8) Metrics & Observability

- **Latency p95**, **tokens_per_doc**, **%docs_invoking_LLM**, **explainability rate**  
- JSON structured logs; per‑analysis metrics row written at job finish.  
- Admin metrics page in web app.

---

## 9) Security & Privacy

- LLM **provider=none** by default; snippet‑only gate if enabled.  
- Signed upload URLs; server‑side MIME & size checks.  
- No PII retained unless retention toggled on.  
- Export includes file checksum + timestamp for chain‑of‑custody.

---

## 10) Windows‑Only Dev Setup (local)

> Run commands in **PowerShell** from the repo root.

### Backend (FastAPI)
```powershell
# Python 3.11 recommended
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r apps\api\requirements.txt
$env:CORE_CONFIG_PATH = "$(Get-Location)\core-config.yaml"
uvicorn blackletter_api.main:app --app-dir apps\api --reload --host 127.0.0.1 --port 8000
```

### Frontend (Next.js)
```powershell
cd apps\web
npm ci
npm run dev
# Web: http://localhost:3000  API: http://localhost:8000
```

### Seed config
Create **core-config.yaml** at repo root:
```yaml
llm:
  provider: none
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
```

---

## 11) Deployment (minimal)

- **DB**: start with SQLite file; for cloud, migrate to Postgres (Supabase) using Alembic.
- **API hosting**: any Windows‑compatible VM or managed service; run `uvicorn` behind reverse proxy.
- **Web hosting**: Next.js build → static export + server routes on same VM.
- **Object storage**: Supabase/Cloudflare R2 for artefacts.

---

## 12) Test Strategy

- **Unit**: detectors (3 positive + 3 hard negative per detector to start), extraction, evidence windows.  
- **Integration**: end‑to‑end upload → findings; snapshot selected responses.  
- **UI**: Playwright flows for upload, findings table, export.  
- **Performance**: latency p95 on 10MB PDFs; token‑budget adherence tests.

---

## 13) Dev Load Always Files (for agents)

List of files agents should always load for context:
- `docs/architecture/tech_stack.md`  
- `docs/architecture/coding_standards.md`  
- `docs/architecture/source_tree.md`  
- `core-config.yaml`  
- `apps/api/blackletter_api/rules/art28_v1.yaml`  
- `apps/api/blackletter_api/rules/lexicons/weak_language.yaml`

*(These three markdown docs should be authored now from this spec; see Appendix B templates.)*

---

## 14) Risks & Mitigations

- **Extraction variance** → PyMuPDF primary, graceful fallbacks, explicit error codes.
- **Clause phrasing variance** → broad anchor families + weak‑language; later tiny classifier.
- **Token blowups** → snippet gates; hard caps; local cache; OCR off by default.
- **False reassurance** → never green without anchor; always display rule id + snippet.

---

## Appendix A — Optional OCR on Windows (off by default)

1) Install **Tesseract for Windows** (e.g., from official installer).  
2) Add to PATH; verify: `tesseract --version`.  
3) `pip install pytesseract pillow`  
4) Set `ocr.enabled: true` in `core-config.yaml` to allow OCR path.

---

## Appendix B — Templates to create now

### docs/architecture/tech_stack.md
- List the locked versions above; justify choices in 1‑2 lines each.

### docs/architecture/coding_standards.md
- Python: Ruff/Black, pydantic v2, async guidelines.  
- TS/React: hooks, React Query, file naming, test conventions.

### docs/architecture/source_tree.md
- Copy the Source Tree section, plus rules on where new modules live.

---

## Appendix C — Story Handover Readiness

- Architecture is compatible with PRD Epics 1–5.  
- **SM** can now draft Story 1.1–1.3 and 2.1–2.4 using this spec.  
- **PO** should approve the first 2–3 stories for Dev to start.

