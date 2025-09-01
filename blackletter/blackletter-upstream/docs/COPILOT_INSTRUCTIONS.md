# Blackletter – VS Code Copilot Pack (OSS + n8n)

This file gives GitHub Copilot (and any human dev) everything needed to understand **who we are**, **what we’re building**, **our stack (OSS-first + n8n)**, and **the exact task to ship next**.

---

## 0) Who You’re Building For (Founder Context)

* **Founder**: 22-year-old London-based law grad building **Blackletter Systems**—practical legal automation.
* **Voice & Values**: Plain English > legalese. Ship fast, stay compliant. Bias to open-source + low-cost infra.
* **Short-term goal (Aug–Oct 2025)**: Reach an MVP that real firms can trial; close 1–3 pilot customers.
* **Business angle**: Productised micro-SaaS + done-for-you automation; legal niche workflows.

---

## 1) Product at a Glance

**Tagline**: *Old rules. New game.*
**Core modules** (each separately deployable):

1. **AI Contract Review** – upload → OCR → clause detect → risk score vs YAML playbook → redlines + summary.
2. **Compliance Checklist** – ingest ICO/FCA/EU/gov feeds → summarise → sector checklists → weekly PDF/email.
3. **Research Assistant (RAG)** – semantic search over BAILII + legislation.gov.uk → answers with para-level cites.

**Acceptance (MVP)**

* Contract: flags key clauses; generates coherent redlines.
* Research: ≥2 primary authorities with paragraph-level citations.
* Compliance: ≥5 actionable tasks per update batch with links + dates.

---

## 2) OSS-First Architecture (+ n8n)

### 2.1 Overview

* **Frontend**: Next.js 14 (TypeScript)
* **Backend**: FastAPI (Python 3.11)
* **DB**: Postgres (Docker)
* **Object Storage**: MinIO (S3-compatible)
* **Vector DB**: Weaviate **or** Qdrant
* **Search (optional)**: Meilisearch
* **Auth**: Supabase Auth (email magic link) **or** Keycloak (self-hosted)
* **LLMs**:

  * Default: OpenAI/Anthropic via env flags (commercial).
  * OSS path: **Ollama** (Llama 3.1, Granite Code) running locally; backend abstracts provider via adapter.
* **OCR**: Tesseract (pytesseract) + pdfplumber/pypdf fallback.
* **Docs/PDF**: Gotenberg (HTML→PDF) for checklists; `python-docx` for redlines.
* **Automations**: **n8n** orchestrates feeds, webhooks, ETL, notifications.

### 2.2 Services (docker-compose excerpt)

```yaml
version: "3.8"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: blackletter
      POSTGRES_PASSWORD: blackletter
      POSTGRES_DB: blackletter
    volumes:
      - db_data:/var/lib/postgresql/data
    ports: ["5432:5432"]

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: adminadmin
    volumes:
      - minio_data:/data
    ports: ["9000:9000", "9001:9001"]

  weaviate:
    image: semitechnologies/weaviate:1.25.7
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"
      PERSISTENCE_DATA_PATH: /var/lib/weaviate
    volumes:
      - weaviate_data:/var/lib/weaviate
    ports: ["8081:8080"]

  meilisearch:
    image: getmeili/meilisearch:v1.8
    environment:
      MEILI_NO_ANALYTICS: "true"
    volumes:
      - meili_data:/meili_data
    ports: ["7700:7700"]

  gotenberg:
    image: gotenberg/gotenberg:8
    command: ["gotenberg", "--chromium-disable-javascript=true"]
    ports: ["3001:3000"]

  n8n:
    image: n8nio/n8n:latest
    ports: ["5678:5678"]
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      N8N_BASIC_AUTH_ACTIVE: "true"
      N8N_BASIC_AUTH_USER: admin
      N8N_BASIC_AUTH_PASSWORD: adminadmin

  backend:
    build: ./src/backend
    env_file: .env
    ports: ["8000:8000"]
    depends_on: [db, minio, weaviate]

  frontend:
    build: ./frontend
    env_file: .env
    ports: ["3000:3000"]
    depends_on: [backend]

volumes: { db_data: {}, minio_data: {}, weaviate_data: {}, meili_data: {}, n8n_data: {} }
```

### 2.3 Env (.env template)

```
# Backend
DATABASE_URL=postgresql+psycopg://blackletter:blackletter@localhost:5432/blackletter
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=admin
S3_SECRET_KEY=adminadmin
S3_BUCKET=blackletter
VECTOR_PROVIDER=weaviate
WEAVIATE_URL=http://localhost:8081
SEARCH_URL=http://localhost:7700
PDF_SERVICE_URL=http://localhost:3001
LLM_PROVIDER=ollama        # choices: openai|anthropic|ollama
OPENAI_API_KEY=            # if LLM_PROVIDER=openai
ANTHROPIC_API_KEY=         # if LLM_PROVIDER=anthropic
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LLM=llama3.1:8b

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# n8n
N8N_URL=http://localhost:5678
N8N_USER=admin
N8N_PASS=adminadmin
```

---

## 3) Repository Structure

```
blackletter/
  src/
    backend/
      app/
        routers/
          contracts.py
          compliance.py
          research.py
        core/
          llm_adapter.py       # openai|anthropic|ollama via one interface
          ocr.py               # pdfplumber + pytesseract
          storage.py           # MinIO S3 client
          vectors.py           # Weaviate/Qdrant client
          redact.py            # docx redlining helpers
          citations.py         # para-level citation enforcement
        services/
          contract_review.py
          compliance_ingest.py # also exposes webhooks for n8n
          research_query.py
        models/
          schemas.py
      main.py
      requirements.txt
  frontend/
    app/
      upload/
      compliance/
      research/
    components/
    lib/api.ts
  n8n/
    workflows/
      compliance_ingest.json      # feeds → dedupe → DB → email trigger
      contract_webhook.json       # webhook → S3 → queue job
  docs/
    PLAYBOOK_SAMPLE.yaml          # risk rules
    CONTRIBUTING.md
    ARCHITECTURE.md
    COPILOT_INSTRUCTIONS.md
    ROADMAP.md
  docker-compose.yml
  .env.example
```

---

## 4) Copilot: How to Help (Put this in `/docs/COPILOT_INSTRUCTIONS.md`)

**Mission**: Generate code that ships the three core modules using the OSS stack + n8n. Prefer simple, testable functions. Add Windows-friendly scripts.

**Style**: Type hints, docstrings, small composable functions. Avoid magic. Write unit tests for pure logic. Use dependency injection for providers.

**When coding**:

* If touching OCR or vectors, call adapters in `core/` rather than hard-coding vendors.
* Always write to MinIO (S3) for any uploaded/generated file. Return S3 keys to frontend.
* For research answers, include `citations=[{case_id, para}]` with paragraph-level references.
* For contract redlines, create `.docx` via `python-docx` and store alongside `review.json` + `summary.md`.
* Emit events (`POST /events`) for n8n to consume when a job completes.

**Test data**: add fixtures under `src/backend/tests/fixtures/` including sample NDAs, leases, and BAILII snippets.

**Edge cases**: low-quality scans, missing pages, multi-language PDFs, tables.

---

## 5) n8n Automations (Workflows to Import)

1. **Compliance Feed Ingest**

   * **Trigger**: Schedule daily 06:00 Europe/London.
   * **Nodes**: HTTP Request (RSS/Atom) → Function (dedupe by URL hash) → LLM Summarise (via backend endpoint) → Postgres Insert (items & tags) → Gotenberg Render (weekly batch) → Email (Resend/SMTP).

2. **Contract Upload Pipeline**

   * **Trigger**: Webhook `/n8n/contract-uploaded` (called by backend after S3 put).
   * **Nodes**: Function (assemble job payload) → Backend `/process/contract` → Wait → On success send email + Slack → Store artifacts index.

3. **RAG Corpus Builder**

   * **Trigger**: Manual + weekly schedule.
   * **Nodes**: HTTP (download judgments) → Split in Batches → Backend `/ingest/document` → Update Weaviate → Log to DB.

> See `n8n/workflows/*.json`. Credentials live in n8n UI; use env from `.env` as defaults.

---

## 6) Windows Dev Bootstrap (PowerShell)

### 6.1 Prereqs

* **Windows 11** (Developer Mode ON)
* **Docker Desktop**, **Git**, **Node 20+**, **Python 3.11**, **Make** (via `choco install make`)
* **Tesseract OCR** (`choco install tesseract`)
* **Ollama** (optional for OSS LLMs)

### 6.2 Commands

```powershell
# Clone
git clone https://github.com/<you>/blackletter.git
cd blackletter

# Env
Copy-Item .env.example .env

# Bring up infra
docker compose up -d db minio weaviate meilisearch gotenberg n8n

# Backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r src\backend\requirements.txt
uvicorn backend.main:app --reload --port 8000 --app-dir src

# Frontend
cd frontend
npm install
$env:NEXT_PUBLIC_API_URL="http://localhost:8000"
npm run dev
```

**Local URLs**

* API docs: `http://localhost:8000/docs`
* UI: `http://localhost:3000/{upload|research|compliance}`
* n8n: `http://localhost:5678` (admin/adminadmin)
* MinIO Console: `http://localhost:9001`

---

## 7) Current Sprint ("Integrate OSS + n8n")

**Goal**: Replace proprietary bits with OSS, wire **n8n** automations, and prove E2E flows.

### 7.1 Issues (create in GitHub)

1. **LLM Adapter – Ollama support**

   * Add `ollama` client, env flags, and model selector; unit tests.
2. **OCR Pipeline**

   * Implement `core/ocr.py` using pdfplumber → pytesseract, with DPI upscaling; tests using sample PDFs.
3. **MinIO Storage**

   * `core/storage.py` S3 put/get; signed URL helper; bucket bootstrap script.
4. **Vectors – Weaviate client**

   * Create schema, upsert chunks, similarity search; ingestion endpoint.
5. **Contract Review Service**

   * Endpoints: `/contracts/review`, `/contracts/redlines`; produce `summary.md`, `review.json`, `redlined.docx`.
6. **n8n – Contract Upload Webhook**

   * Backend emits `POST http://localhost:5678/webhook/contract-uploaded` with {s3\_key, doc\_type}.
7. **Compliance Ingest**

   * Backend `/compliance/ingest` (LLM summariser) used by n8n feed flow. Store items in Postgres.
8. **RAG Corpus**

   * `/ingest/document` → chunk → embed → upsert Weaviate. Query path used by `/research/query`.

### 7.2 Definition of Done

* `docker compose up` + minimal manual steps gets all services running locally on Windows.
* n8n workflows imported and successfully trigger backend endpoints.
* Example NDA processed: artifacts saved in MinIO; notification fired.

---

## 8) Do/Don’t (for Copilot + Contributors)

✅ **Do**

* Keep adapters vendor-agnostic; everything behind `core/*`.
* Log decisions in PR description; update `ARCHITECTURE.md` when interfaces change.
* Prefer simple YAML playbooks for legal rules; keep them versioned in `/docs`.

❌ **Avoid**

* Hardcoding API keys.
* Writing to local disk for artifacts (use S3/MinIO).
* Embedding PDFs without chunking (target 1–2k tokens).

---

## 9) Roadmap (90 Days)

* **Week 1–2**: Ship adapters (OCR, vectors, storage, LLM). Import n8n flows. Process first NDA.
* **Week 3–4**: RAG ingestion; paragraph-level citations; compliance weekly PDF.
* **Month 2**: Auth + multi-tenant; audit logs; export client packs; pricing page.
* **Month 3**: Pilot with 2–3 firms; refine playbooks; add Stripe; harden security.

---

## 10) VS Code Setup (workspace)

* Extensions: GitHub Copilot & Chat, Python, Pylance, Ruff, Docker, YAML, ESLint, Prettier, Thunder Client, Makefile Tools.
* `.vscode/settings.json` (suggested):

```json
{
  "python.defaultInterpreterPath": ".\\.venv\\Scripts\\python.exe",
  "editor.formatOnSave": true,
  "files.trimTrailingWhitespace": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "ruff.lint.args": ["--fix"],
  "terminal.integrated.defaultProfile.windows": "PowerShell"
}
```

* **Copilot Chat quick context**: “Read `/docs/*`, `/src/backend/app/core/*`, and `/n8n/workflows/*` before generating code.”

---

## 11) Quick Start Tasks for Copilot (paste in chat)

1. *“Generate **`core/llm_adapter.py`** with providers: openai, anthropic, ollama. Include a **`generate(text, system, model)`** function and provider registry from env.”*
2. *“Implement **`core/ocr.py`** (pdfplumber, pytesseract) that returns plain text + clause-level page spans.”*
3. *“Write **`services/contract_review.py`** that uses OCR → clause heuristics (regex for termination/assignment/repair/rent review/insurance) → score vs YAML playbook → produce markdown summary + JSON risks + redlined .docx.”*
4. *“Create FastAPI endpoints in **`routers/contracts.py`** calling the above and storing artifacts in MinIO.”*
5. *“Export an n8n webhook client in backend to **`POST /webhook/contract-uploaded`** with job metadata.”*

---

## 12) Security & Compliance (MVP)

* Least-privilege MinIO keys; 30-day retention; antivirus scan on upload (ClamAV container optional).
* Audit table for every document access; redact PII in logs.
* Configurable data residency fields in DB for future multi-region.

---

## 13) Business Ops Automations (n8n)

* **Lead capture → CRM**: Web form → n8n → Postgres/HubSpot (free) → email acknowledgement.
* **Weekly usage report**: Cron → query DB → PDF via Gotenberg → email to founder.
* **Error alerts**: n8n catches webhook errors from backend; post to Slack/Discord.

---

## 14) Open Questions (for future PRDs)

* Final choice between Weaviate vs Qdrant.
* Supabase Auth vs Keycloak (self-host tradeoffs).
* Which OSS LLM models meet quality for legal text locally (may require remote API initially).

---

**That’s the pack.** Create the files under `/docs`, add the adapters, import the n8n JSONs, and ship the Contract Upload flow first.

