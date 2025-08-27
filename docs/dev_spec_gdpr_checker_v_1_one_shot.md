# Blackletter Systems — GDPR Processor Checker v1 (One‑Shot Dev Spec)

> Purpose: Give a single engineer everything needed to build the MVP that runs 8 GDPR Art.28(3) checks end‑to‑end (Upload → Detect → Review → Export) with explainable, auditable outputs under p95 ≤ 60s/doc and ≈£0.10/doc.

---

## 0) Scope & Non‑Goals
**In‑scope**
- Upload PDF/DOCX (≤10MB). No OCR by default.
- Deterministic detectors (8 core checks mapped to GDPR Art.28(3)(a–h)).
- Evidence‑first UI: Findings table, verdict chips (Pass/Weak/Missing/Needs review), Evidence Drawer (snippet + rule id), filters by verdict.
- Export HTML/PDF report.
- Optional LLM (snippet‑only) for short rationales. Disabled by default; hard token caps.

**Out of scope (v1)**
- Deep clause rewriting/negotiation suggestions.
- Multi‑doc batching; OCR; non‑English.
- Persistent DB beyond local JSON files.

---

## 1) Architecture Overview
Monorepo (JS/TS web + Python API). Local‑first. All processing on the API.

```
repo/
  apps/
    web/                      # Next.js 14 (App Router)
      src/app/
        upload/page.tsx
        dashboard/page.tsx    # Analyses list
        analyses/[id]/page.tsx# Findings + Evidence Drawer + Export
      src/lib/{api.ts,types.ts,store.ts}
    api/
      blackletter_api/
        main.py               # FastAPI entry
        routers/
          analyses.py         # REST endpoints
        services/
          extract.py          # PDF/DOCX → text + page map
          detect.py           # Detector runner
          llm.py              # Optional snippet-only rationale
          export.py           # HTML/PDF report gen
        models/
          schemas.py          # Pydantic models (Analysis, Finding)
        rules/
          rulepacks/art28_v1.yaml
          lexicons/weak.yaml
        storage/
          analyses/           # JSON payloads per analysis id (MVP)
  packages/
    fixtures/                 # detector test fixtures (3 pos/3 neg)
  .env.example
  README.md
```

---

## 2) User Flow (System)
```
Upload (PDF/DOCX) → Extract text + page map → Sentence index (±2 window)
→ Detector Runner (anchors/weak/redflags)
→ Findings Table (filter by verdict) ⇄ Evidence Drawer (snippet+rule_id)
→ Export (HTML/PDF) + Metrics (p95, tokens, explainability)
```

---

## 3) APIs (FastAPI)
### 3.1 Routes
- `POST /api/contracts` → start analysis
  - Body: multipart form with `file`
  - Returns: `{ analysis_id }`
- `GET /api/analyses/{analysis_id}` → analysis summary
  - Returns: `Analysis` (status, doc meta, metrics)
- `GET /api/analyses/{analysis_id}/findings` → list findings
  - Returns: `Finding[]`
- `POST /api/reports/{analysis_id}` → generate report
  - Body: `{ format: "html" | "pdf" }`
  - Returns: `{ url }` (path to report)

### 3.2 Models (Pydantic)
```python
class Finding(BaseModel):
  detector_id: str
  rule_id: str
  verdict: Literal["pass","weak","missing","needs_review"]
  snippet: str
  page: int | None
  start: int | None
  end: int | None
  rationale: str | None

class Analysis(BaseModel):
  id: str
  status: Literal["queued","processing","done","error"]
  filename: str
  created_at: datetime
  metrics: dict  # {p95_ms:int, tokens:int, explainability:float}
```

---

## 4) Detector Engine
### 4.1 Verdict Policy
```json
{
  "verdict_policy": {
    "pass": "anchor_present && !redflag && !weak_nearby",
    "weak": "anchor_present && weak_nearby && !redflag",
    "missing": "!anchor_present || contradicted",
    "needs_review": "ambiguous || over_token_budget || extraction_error"
  },
  "evidence_window_sentences_default": 2
}
```

### 4.2 Rulepack Schema (YAML)
```yaml
rulepack_id: art28_v1
version: 1.0
lexicons:
  weak:
    - commercially reasonable
    - where practicable
    - endeavour
    - may
  redflags:
    - subject solely to provider policies
    - no warranty of security
    - processor may process .* as necessary to operate its services

# 8 detectors a–h
detectors:
  - id: A28_3_a_instructions
    title: Controller instructions only
    anchors_any:
      - only on documented instructions
      - process .* only on .* written instructions
    allowlist_any:
      - unless required by law
    weak_nearby_from_lexicon: weak
    redflags_any_from_lexicon: redflags
    evidence_window_sentences: 2
    rule_id: art28_v1.A28_3_a_instructions

  - id: A28_3_b_confidentiality
    title: Confidentiality obligations
    anchors_any:
      - confidentiality obligations
      - bound by confidentiality
    weak_nearby_from_lexicon: weak
    rule_id: art28_v1.A28_3_b_confidentiality

  - id: A28_3_c_security
    title: Security (TOMs)
    anchors_any:
      - technical and organisational measures
      - appropriate technical .* organisational measures
    redflags_any:
      - no warranty of security
    weak_nearby_from_lexicon: weak
    rule_id: art28_v1.A28_3_c_security

  - id: A28_3_d_subprocessors
    title: Sub‑processor authorization
    anchors_any:
      - prior specific or general written authorisation
      - maintain an up‑to‑date list of subprocessors
    rule_id: art28_v1.A28_3_d_subprocessors

  - id: A28_3_e_data_subject_assist
    title: Assist with data subject rights (Arts. 12–23)
    anchors_any:
      - assist the controller by appropriate technical and organisational measures
      - requests from data subjects
    rule_id: art28_v1.A28_3_e_data_subject_assist

  - id: A28_3_f_breach_notify
    title: Breach notification to controller
    anchors_any:
      - notify the controller without undue delay
      - personal data breach
    rule_id: art28_v1.A28_3_f_breach_notify

  - id: A28_3_g_deletion_return
    title: Return or deletion after end of provision
    anchors_any:
      - delete or return all the personal data
      - upon termination
    allowlist_any:
      - unless Union or Member State law requires storage
    rule_id: art28_v1.A28_3_g_deletion_return

  - id: A28_3_h_audit_info
    title: Audits and information provision
    anchors_any:
      - make available to the controller all information necessary
      - allow for and contribute to audits, including inspections
    rule_id: art28_v1.A28_3_h_audit_info
```

### 4.3 Runner Algorithm (Python sketch)
1) Build sentence index with page & char offsets.
2) For each detector:
   - `anchor_present = any(re_anchor.search(window))`
   - `weak_nearby`/`redflag` using lexicons within ±2 sentences.
   - Apply verdict policy; capture best matching snippet (first anchor hit ± window).
3) Persist `Finding[]` to `storage/analyses/{id}/findings.json`.

---

## 5) Extraction
- **PDF**: PyMuPDF (fitz) for text with page numbers.
- **DOCX**: python‑docx.
- **Sentence split**: simple regex `[.!?]` + newline; keep char offsets; page map from PDF.
- **OCR**: off by default. (Optional later: Tesseract.)

---

## 6) Optional LLM (Snippet‑Only, OFF by default)
- Purpose: turn rule‑based signal into 1–2 lines of readable rationale **without** reading the full document.
- Input: `detector_id`, `rule_id`, `snippet`, `verdict`.
- Hard caps: `max_tokens=200`, 1 call per finding.
- Config: `LLM_ENABLED=false` (default), `LLM_PROVIDER=`, `LLM_API_KEY=`.
- If disabled, populate `rationale` with deterministic template.

---

## 7) Web (Next.js)
### 7.1 Pages & Components
- `/upload` — drag‑and‑drop; posts to `/api/contracts`; redirect to `/analyses/{id}` on success.
- `/dashboard` — list recent analyses (mock or API based on flag).
- `/analyses/[id]` — Findings table with verdict chips; Filters (All/Pass/Weak/Missing/Needs review); Evidence Drawer (snippet + rule id + rationale). Export button (HTML/PDF).

### 7.2 UI State
```ts
export type Verdict = 'pass'|'weak'|'missing'|'needs_review';
export interface Finding { detector_id:string; rule_id:string; verdict:Verdict; snippet:string; page?:number; start?:number; end?:number; rationale?:string }
export interface Analysis { id:string; status:'queued'|'processing'|'done'|'error'; filename:string; created_at:string; metrics:Record<string,unknown> }
```

### 7.3 Styling & UX
- Minimal, evidence‑first. Sticky table header; right‑side drawer.
- Keyboard: up/down navigate findings; `Enter` opens drawer.
- Empty states + loading skeletons.

---

## 8) Export (HTML/PDF)
- HTML template (`templates/report.html`) rendered with findings + metrics.
- PDF rendering via headless Chromium (Playwright) on Windows.
- File saved to `storage/analyses/{id}/report.{html|pdf}`; API returns path.

---

## 9) Performance, Metrics & SLAs
- p95 end‑to‑end ≤ 60s/doc (10‑page PDF baseline on Windows laptop).
- Explainability ≥ 95% (each finding must include snippet + rule_id; track % findings with evidence).
- Cost
  - Deterministic pipeline ≈ £0.00.
  - If LLM enabled: target ≤ £0.10/doc by capping findings × tokens.
- Metrics recorded per analysis: `duration_ms`, `p95_ms` (rolling), `tokens`, `explainability_rate`.

---

## 10) Security, Privacy, Audit
- Local processing; no document content in logs.
- Audit JSON: `storage/analyses/{id}/audit.json` containing rulepack version, checksums, timestamps, env flags.
- PII safe‑logging: only analysis id, status, timings.

---

## 11) Testing & Fixtures
- **Unit (detectors)**: per detector 3 positive / 3 negative sentences in `packages/fixtures/{detector}.yaml`.
- **Integration**: run full pipeline on `fixtures/docs/sample_dpa.pdf` expecting known verdict distribution.
- **UI E2E**: Playwright: upload → view findings → filter → open drawer → export.
- **Performance**: script to time 20 analyses in series; assert p95 ≤ 60s.

---

## 12) Windows Dev Setup (PowerShell)
```powershell
# Prereqs: Node 20+, Python 3.11+, Git, Chrome (for PDF), PowerShell 7

# 1) Clone & install
git clone <repo-url> blackletter
cd blackletter

# Web
cd apps/web
npm ci
cd ../..

# API (venv)
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r apps/api/requirements.txt

# 2) Env
Copy-Item .env.example .env
# Set: NEXT_PUBLIC_USE_MOCKS=1 (to use mocks); LLM_ENABLED=false

# 3) Run dev (two terminals)
# Terminal A (API)
. .venv/Scripts/Activate.ps1
python apps/api/blackletter_api/main.py

# Terminal B (Web)
cd apps/web
npm run dev

# Open http://localhost:3000
```

---

## 13) Acceptance Criteria (MVP)
1. Upload accepts PDF/DOCX ≤10MB; analysis status transitions to `done`.
2. For a seeded DPA fixture:
   - a) instructions → **Pass**
   - b) confidentiality → **Weak** (hedged terms detected)
   - c) security → **Missing** (no TOMs anchor)
   - d–h) produce deterministic verdicts per fixtures.
3. Each finding shows: verdict chip, snippet, rule_id, rationale (LLM off: templated text).
4. Filters work; keyboard navigation works; Evidence Drawer opens with correct snippet.
5. Export produces HTML and PDF with metadata & metrics.
6. p95 ≤ 60s/doc over 20 runs; explainability ≥95%.

---

## 14) Dev Notes
- Keep regexes anchored and case‑insensitive; pre‑compile patterns.
- Evidence window default ±2 sentences; allow per‑detector override.
- All rulepack and lexicon changes bump `version` and are captured in audit JSON.

---

## 15) Seed Data & Demo Path
1) Place `fixtures/docs/sample_dpa.pdf` in repo.
2) Start API + Web (mocks off).
3) Upload the sample; navigate to `/analyses/{id}`.
4) Toggle filters; open Evidence Drawer; Export PDF.

---

## 16) Future (Not Required for MVP)
- OCR via Tesseract + layout‑aware windows.
- Clause rewrite suggestions (LLM‑on) behind feature flag.
- Persistent DB (SQLite → Postgres), auth, multi‑tenant.
- Multi‑doc batching and email export.

