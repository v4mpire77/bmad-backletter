# Blackletter — Application Architecture (Winston v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Owner (Application Architect)**: Winston  
**Date**: 2025‑08‑26  
**Intended Readers**: PM, UX, PO, SM, Dev, QA

> Scope: Receive MVP from the PRD, translate into explicit technical decisions, source tree, version pins, and operational practices. Align with Analyst (Mary) + PM (John) + UX (Sally). Windows‑first commands, low‑cost, explainable, rules‑first; LLM off by default.

---

## 0) MVP Receipt (from PRD)
- 8 GDPR Art. 28(3) detectors (a)–(h) with **Pass / Weak / Missing / Needs review** and citations.  
- Upload PDF/DOCX ≤10MB → async job → Findings table + Evidence Drawer → Export (PDF/HTML).  
- Metrics: p95 latency ≤ 60s; tokens/doc; %LLM usage; explainability rate.  
- Settings: toggle LLM provider (default **none**), OCR, retention.

---

## I. Overall System Architecture & Design

### A. Frontend ↔ Backend Integration
- **Protocol**: REST/JSON over HTTPS.  
- **Client data layer**: React Query (stale‑while‑revalidate, retries, polling).  
- **Auth (MVP)**: Session cookie (httpOnly, secure); roles: Admin/Reviewer.

### B. Processing Orchestration (agentic pipeline → pragmatic modules)
The “multi‑agent” intent maps to explicit services to keep determinism:
1) **Intake Router** → validates file, creates `analysis`, enqueues job.  
2) **Extractor** → PDF/DOCX → text + page map + sentence index (non‑OCR by default).  
3) **Evidence Windower** → offset → ±2 sentences.  
4) **Detector Runner** → YAML rulepack (anchors/weak/red‑flags) → verdict + snippet + offsets + rule id.  
5) **Reporter** → assemble findings + export.  
6) **Metrics Writer** → latency, tokens, %LLM, explainability.

### C. Asynchronous Strategy
- **MVP**: FastAPI `BackgroundTasks` (simple, no external broker).  
- **Phase‑2**: Celery + Redis for durable queues, schedule retries, and fan‑out (e.g., detector parallelism).  
- Interface (`services/tasks.py`): `enqueue(job_type, payload) -> job_id`; pluggable backend.

---

## II. Technology Stack & Core Components (explicit)

> **Pin policy**: lock exact versions at scaffold; record in `versions.lock.md` (+ `pip-tools` and npm lockfile). Below are tested constraints.

### Frontend
- **Node.js**: 20.x (LTS)  
- **Next.js**: 14.2.x  
- **React**: 18.2.x  
- **TypeScript**: 5.4.x  
- **Tailwind CSS**: 3.4.x  
- **shadcn/ui** (+ Radix primitives)  
- **lucide-react** for icons  
- **React Query** for server state  
- **Playwright** + **Vitest** for UI tests

### Backend (Python)
- **Python**: 3.11.x  
- **FastAPI**: 0.111.x  
- **Uvicorn**: 0.30.x  
- **SQLAlchemy**: 2.0.x, **Pydantic**: 2.7.x  
- **PyMuPDF (fitz)**: 1.24.x (PDF), **docx2python**: 2.8.x (DOCX)  
- **blingfire**: 0.1.x (sentence segmentation)  
- **Report**: headless Chromium render for PDF export  
- **Optional OCR**: Tesseract via `pytesseract` (off by default)  
- **Testing**: `pytest`, `pytest-asyncio`  
- **Lint/format**: `ruff`, `black`

### Storage & Infra
- **Local dev**: SQLite + filesystem artefacts.  
- **Cloud**: Postgres (Supabase) + object storage (Supabase Storage / S3‑compatible).  
- **Queue (phase‑2)**: Redis for Celery.  
- **Observability**: structured logs (`structlog`), OpenTelemetry (phase‑2).

### LLM Integration (optional)
- Default **off**; snippet‑only gate.  
- Provider adapter interface allows OpenAI/Anthropic/Gemini; token caps enforced by `core-config.yaml`.

> **RAG**: **Not in MVP.** Rule‑first suffices. If later needed, use Postgres + `pgvector` with scoped embeddings by `org_id` (+ small local embed model).

---

## III. Data Management & Persistence

### A. Database
- **MVP**: SQLite (fast dev, simple deploy).  
- **Phase‑2**: Supabase Postgres; Alembic migrations maintain parity.

### B. File Storage
- **Dev**: `apps/api/.data/analyses/{analysis_id}/...`  
- **Cloud**: Object storage bucket; DB stores pointers & checksums.

### C. Schemas / Shared Types
- Define Pydantic models (`schemas.py`) and generate TS types for web via OpenAPI or `datamodel-codegen`.  
- **Issue/Finding model** shared shape ensures strict FE/BE contract.

### D. Multi‑tenancy
- Add `org_id` to `analysis`, `finding`, storage paths, and (future) vector tables; enforce row‑level scoping in queries.

---

## IV. API Design & Data Flow (contract‑first)

**Base**: `/api` (FastAPI)

### POST `/api/contracts`
Create analysis + job.
- **Req**: multipart form: `file` PDF/DOCX (≤10MB)  
- **201**: `{ job_id, analysis_id, status: "queued" }`  
- **Errors**: 400 size/type; 415 unsupported; 500 extraction error.

### GET `/api/jobs/{job_id}`
- **200**: `{ job_id, status: "queued|running|done|error", error? }`

### GET `/api/analyses/{analysis_id}`
- **200**: summary: filename, created_at, verdicts per detector (8 rows).

### GET `/api/analyses/{analysis_id}/findings`
- **200**: `Finding[]` (see model below)

### POST `/api/reports/{analysis_id}`
- **201**: `{ url }` (PDF/HTML generated)

#### Finding (Issue) model (Pydantic → TS)
```json
{
  "detector_id": "A28_3_c_security",
  "rule_id": "art28_v1.A28_3_c_security",
  "verdict": "pass|weak|missing|needs_review",
  "snippet": "Processor shall… technical and organisational measures…",
  "page": 7,
  "start": 1423,
  "end": 1562,
  "rationale": "anchor present; no red‑flag",
  "reviewed": false
}
```

### Realtime / Progress
- **MVP**: React Query polling `GET /jobs/{id}`; poll 1s–2s backoff.
- **Phase‑2**: SSE endpoint for push updates (WebSockets optional).

---

## V. Performance, Scalability & Observability

### Targets
- p95 ≤ 60s per ≤10MB PDF; ≤ £0.10/document at defaults.

### Concurrency
- Run Uvicorn with `--workers N` (CPU‑bound tasks avoided; I/O heavy).  
- Detector runner supports **sequential** MVP; optional fan‑out per detector in Celery (phase‑2).

### Cost Guardrails
- Token ledger; snippet size caps; provider off by default; cache by `(prompt_id, snippet_hash)`; OCR off unless enabled.

### Logging & Metrics
- JSON logs with job spans; per‑analysis metrics row (latency_ms, tokens_used, llm_invoked, explainability_hit).  
- Admin metrics page consumes `/api/admin/metrics` (simple aggregate in MVP).

---

## VI. Security & Development Practices

### Secrets
- `.env` files (Windows‑safe) + environment variables; no secrets in repo.  
- Future: Secret manager (Azure Key Vault / AWS Secrets Manager) abstraction.

### Data Minimization
- If LLM enabled, **redact PII** in snippet pre‑processor (regex class + allowlist).  
- Never send full document; only snippet windows.

### Coding Standards
- **Backend**: `ruff` + `black`; `mypy` optional; async services; no business logic in routers.  
- **Frontend**: ESLint + Prettier; functional components; `useQuery` hooks in `web/lib`.

### Testing Strategy
- **Unit**: detectors (3 pos + 3 hard neg per detector), extractor, windower.  
- **Integration**: upload → findings happy path.  
- **E2E**: Playwright run for Upload → Findings → Export.  
- **Golden outputs**: fixtures under `tests/fixtures/gold/` with checksums.

### Windows‑only Dev
- Provide PowerShell scripts under `/scripts/ps/` for setup, run, test, lint.  
- Use `py -3.11` launcher; avoid Bash‑only scripts.

---

## VII. Source Tree (explicit)
```
blackletter/
  apps/
    web/                       # Next.js 14 app
      app/
      components/
      lib/
      styles/
      public/
      package.json
      tsconfig.json
    api/                       # FastAPI service
      blackletter_api/
        main.py
        config.py
        core_config_loader.py  # loads core-config.yaml
        routers/
          uploads.py
          jobs.py
          analyses.py
          reports.py
        services/
          tasks.py             # enqueue/worker interfaces
          extraction.py        # PDF/DOCX → text, page map, sentence index
          evidence.py          # ±2 sentence windows
          detection.py         # rulepack runner, verdict mapping
          reporting.py         # export assembly
          metrics.py
        rules/
          art28_v1.yaml
          lexicons/
            weak_language.yaml
        models/
          db.py                # SQLAlchemy engine/session
          entities.py          # ORM models
          schemas.py           # Pydantic I/O models
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
  core-config.yaml
  versions.lock.md
  scripts/
    ps/
      dev.ps1                 # run web+api
      test.ps1                # run all tests
      lint.ps1                # ruff/black/eslint
  README.md
```

---

## VIII. Version Pin Matrix (record at scaffold)

| Area | Package | Version (pin) |
|---|---|---|
| Node | node | 20.x |
| Web | next | 14.2.x |
| Web | react | 18.2.x |
| Web | typescript | 5.4.x |
| Web | tailwindcss | 3.4.x |
| Web | @tanstack/react-query | 5.x |
| Web | lucide-react | 0.x |
| API | fastapi | 0.111.x |
| API | uvicorn | 0.30.x |
| API | sqlalchemy | 2.0.x |
| API | pydantic | 2.7.x |
| API | pymupdf | 1.24.x |
| API | docx2python | 2.8.x |
| API | blingfire | 0.1.x |

> On first commit, run `pip freeze > versions.lock.md` (append Python block) and `npm ls --depth=0 >> versions.lock.md` (append JS block) to capture exacts.

---

## IX. Trade‑offs & Alternatives
- **BackgroundTasks vs Celery**: simpler vs durable retries & parallelism. Start simple; feature‑flag Celery.  
- **SQLite vs Postgres**: fastest dev vs concurrency & scale; migrate behind repository layer.  
- **PDF render**: headless Chromium (consistent CSS) vs wkhtmltopdf (lighter but CSS quirks).  
- **LLM provider**: adapter with token caps; default none; switchable via env.

---

## X. Windows‑Only Commands (local)

### API
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r apps\api\requirements.txt
$env:CORE_CONFIG_PATH = "$(Get-Location)\core-config.yaml"
uvicorn blackletter_api.main:app --app-dir apps\api --reload --host 127.0.0.1 --port 8000
```

### Web
```powershell
cd apps\web
npm ci
npm run dev
# Web: http://localhost:3000  |  API: http://localhost:8000
```

### Scripts
```powershell
scripts\ps\dev.ps1    # run both
scripts\ps\test.ps1   # run all tests
scripts\ps\lint.ps1   # ruff/black/eslint
```

---

## XI. Dev‑Load‑Always Files (for agents)
- `docs/architecture/tech_stack.md`  
- `docs/architecture/coding_standards.md`  
- `docs/architecture/source_tree.md`  
- `core-config.yaml`  
- `apps/api/blackletter_api/rules/art28_v1.yaml`  
- `apps/api/blackletter_api/rules/lexicons/weak_language.yaml`

---

## XII. Ready‑for‑PO Validation
- PRD ↔ Architecture ↔ UX coherent on: uploads, findings, exports, metrics, settings.  
- First stories ready for PO approval: **1.1–1.3**, **2.1–2.2**, **3.1–3.2**.  
- Risks, performance targets, and cost guardrails encoded in config + tests.

