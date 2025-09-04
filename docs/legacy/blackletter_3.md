# Blackletter 3.0 — Clean‑Slate Repo & Migration Playbook (MVP → Phase 2)

**Audience**: Vibe CEO, Winston (App Arch), Sally (UX), Sarah (PO), Sam (SM), James (Dev), Quinn (QA)  
**Goal**: Stop the thrash from a messy legacy repo. Stand up a clean, production‑minded MVP now, then safely **strangler‑migrate** anything truly valuable from the old codebase.

---

## 0) Executive Decision (TL;DR)
**Yes — create a new repo** for *Blackletter 3.0*. Treat the old repo as a **read‑only artifact mine**. We’ll:
1) Ship MVP from a clean skeleton using the BMAD V4 process.
2) Inventory the legacy repo, extract only **proven** units behind adapters.
3) Delete dupes & noise via a scripted audit (hash‑based + path rules).

> Rationale: reduces cognitive load, enables crisp CI gates, prevents “mystery regressions,” and gives us deterministic docs→code flow.

---

## 1) New Repo Layout (clean skeleton)
```
blackletter/
  apps/
    web/                       # Next.js 14 + shadcn/ui
      app/
      components/
      lib/
      styles/
      public/
      package.json
      tsconfig.json
    api/                       # FastAPI 0.111 (Python 3.11)
      blackletter_api/
        main.py
        config.py
        core_config_loader.py
        routers/
          uploads.py
          jobs.py
          analyses.py
          reports.py
        services/
          tasks.py
          extraction.py
          evidence.py
          detection.py
          reporting.py
          llm_gate.py
          metrics.py
        rules/
          art28_v1.yaml
          lexicons/
            weak_language.yaml
        models/
          db.py
          entities.py
          schemas.py
        tests/
          unit/
          integration/
      pyproject.toml
      requirements.txt
  docs/
    prd.md
    architecture.md
    uiux.md
    po-validation.md
    stories/
  tools/
    score_goldset.py
  scripts/
    ps/
      dev.ps1
      test.ps1
      lint.ps1
  core-config.yaml
  versions.lock.md
  .github/workflows/
    backend.yml
    frontend.yml
  .editorconfig
  .gitattributes
  .gitignore
  README.md
```

**Pins**: Record Python + npm dep trees into `versions.lock.md` on first commit.

---

## 2) MVP System Architecture (lock‑in)
- **Frontend**: Next.js 14 (App Router), TS 5, Tailwind, shadcn/ui, React Query.
- **Backend**: FastAPI 0.111, Uvicorn, SQLAlchemy 2, Pydantic v2.
- **Extraction**: PyMuPDF (PDF), docx2python (DOCX), blingfire (sentences). OCR off by default.
- **Detection**: Rules‑first `art28_v1.yaml` (detectors a–h) + `weak_language.yaml`. Evidence window ±2 sentences.
- **Export**: HTML→PDF via headless Chromium.
- **Store**: SQLite dev (file); Postgres (Supabase) Phase 2.
- **Async**: FastAPI `BackgroundTasks` MVP; Celery + Redis Phase 2.
- **Metrics**: p95 latency, tokens/doc, %LLM usage, explainability rate.
- **Security**: LLM provider **none** by default; snippet‑only if enabled; PII redaction pre‑LLM.

**API Contracts (MVP)**
- `POST /api/contracts` → `{ job_id, analysis_id, status }`
- `GET /api/jobs/{job_id}` → status
- `GET /api/analyses/{id}` → summary + coverage
- `GET /api/analyses/{id}/findings` → `Finding[]`
- `POST /api/reports/{analysis_id}` → `{ url }`

**Finding (authoritative)**
```json
{ "detector_id":"A28_3_c_security", "rule_id":"art28_v1.A28_3_c_security", "verdict":"pass|weak|missing|needs_review", "snippet":"…", "page":7, "start":1423, "end":1562, "rationale":"anchor present; no red‑flag", "reviewed":false }
```

---

## 3) BMAD V4 in Terminal (CLI path)
1) **Initialize BMAD core** in the new repo root:
   ```bash
   npx bmad-method install
   # choose: Complete installation → select IDE(s) → skip web bundles
   ```
2) **Shard docs** (after you paste PRD/Arch/UI/PO into `docs/`):
   ```
   *shard-doc docs/prd.md prd
   *shard-doc docs/architecture.md architecture
   ```
3) **Agent flow (each in a fresh chat/tab)**:
   - **SM**: open *Scrum Master Story Pack* → pick Story **1.1**.
   - **Dev**: implement story exactly; commit; mark “ready for review”.
   - **QA**: verify against acceptance; mark “done”.
   - Loop: **1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 3.1 → 3.2 → 2.4 → 4.1 → 4.2 → 5.1 → 5.2**.

> Keep **dev‑load‑always**: `docs/architecture/tech_stack.md`, `coding_standards.md`, `source_tree.md`, `core-config.yaml`, and the rulepack files.

---

## 4) Hindsight‑is‑20/20 Guardrails (If only we had…)
1) **Pins from day zero** → `versions.lock.md` + CI cache keys.  
2) **One story per PR**, include acceptance criteria in PR body; block merges without QA check.  
3) **Pre‑commit hooks**: ruff/black + eslint/prettier + type‑check.  
4) **Secrets**: git‑secrets scan; forbid committing `.env`.  
5) **Golden tests**: snapshot a known DPA → freeze runner output; fail on drift.  
6) **Error codes table** → shared UI/API copy; no ad‑hoc strings.  
7) **Export templating** → server‑side only; deterministic fonts.  
8) **Hard token caps** → caps as config, not code; log cap hits.  
9) **Docs sharded** → agents never load whole megafile.  
10) **Conventional Commits** + PR template referencing Story IDs.  
11) **Read‑only legacy** → salvage behind adapters; no direct imports.  
12) **Branch protections** → tests + lint green required; codeowners for critical paths.

---

## 5) MVP Delivery Plan (2 sprints)
**Sprint A (Foundations)**  
- 1.1 Upload & Jobs  
- 1.2 Extraction  
- 1.3 Evidence Windows  
- 2.1 Rulepack Loader  
- 2.2 Detector Runner  
**Exit**: Findings appear for baseline PDFs; unit/integration tests pass.

**Sprint B (UX & Ops)**  
- 3.1 Findings Table UI  
- 3.2 Report Export  
- 2.4 Token Ledger & Caps  
- 4.1 Metrics Wall  
- 4.2 Coverage Meter  
- 5.1 Settings  
- 5.2 Minimal Auth  
**Exit**: Export works; metrics tiles live; coverage 8/8; AA contrast; role gating.

**MVP Gates**: p95 ≤ 60s/doc; ≤ £0.10/doc; Precision ≥ 0.85; Recall ≥ 0.90; Explainability ≥ 95%.

---

## 6) Phase 2 (Scale & Niceties)
- **Infra**: Celery + Redis; migrate to Postgres (Supabase) with Alembic.  
- **Realtime**: switch to SSE for job progress.  
- **Auth**: SSO (Supabase auth / NextAuth).  
- **RAG (if really needed)**: Postgres + pgvector; embeddings scoped by `org_id`.  
- **Coverage expansion**: detectors beyond Art. 28(3); multilingual; OCR defaults for scans.  
- **Observability**: OpenTelemetry traces; structured logs shipping.

---

## 7) Legacy Repo → Migration Strategy (Strangler Fig)
**Objective**: Safely pull across only **working, proven** components.

1) **Freeze** legacy repo to read‑only; tag it `legacy-final`.
2) **Inventory**: run audit scripts (below) → CSV of file types, sizes, dupes, top‑level modules.  
3) **Quarantine**: create `legacy_lab/` in the new repo (git‑ignored) for temporary drops.  
4) **Adapter Harness**: write small adapters to our new contracts (e.g., convert old extraction result → `ExtractionArtifact`).  
5) **Porting Order**:
   - (a) Extractors that pass our tests faster/cleaner than current.  
   - (b) Any deterministic rule checks that match our schema.  
   - (c) Utility libs (logging, parsing) with low coupling.  
6) **Tests First**: create contract tests; run old code under harness; only merge if **all** acceptance criteria pass and performance is ≥ current.  
7) **Deprecate**: document what *not* to port and why.

**Do NOT** import legacy modules directly into production paths. Everything flows through an adapter that enforces current interfaces.

---

## 8) Repo Audit & De‑duplication (Scripts)

### A) Hash‑based duplicate finder (PowerShell)
```powershell
Get-ChildItem -Path . -Recurse -File |
  Where-Object { $_.Length -gt 0 } |
  ForEach-Object {
    $hash = Get-FileHash $_.FullName -Algorithm SHA256
    [PSCustomObject]@{ Path=$_.FullName; Hash=$hash.Hash; Size=$_.Length }
  } |
  Group-Object Hash |
  Where-Object { $_.Count -gt 1 } |
  ForEach-Object { $_.Group | Select-Object Path,Size,Hash } |
  Export-Csv .\dupes.csv -NoTypeInformation
```

### B) Language/type census
```powershell
Get-ChildItem -Recurse -File |
  Group-Object { $_.Extension.ToLower() } |
  Sort-Object Count -Descending |
  Select-Object Name,Count |
  Export-Csv .\file_types.csv -NoTypeInformation
```

### C) Large files & binaries (purge candidates)
```powershell
Get-ChildItem -Recurse -File |
  Where-Object { $_.Length -gt 10MB } |
  Select-Object FullName, Length |
  Export-Csv .\big_files.csv -NoTypeInformation
```

**Rule of thumb**: only carry forward code that (1) compiles, (2) has tests or is trivially testable, (3) matches new contracts with minimal shim.

---

## 9) Testing & Quality Gates
- **Unit**: detectors (≥3 pos + ≥3 hard neg per a–h), extraction, windower.  
- **Integration**: upload→findings→export happy path.  
- **E2E**: Playwright flows for Upload, Findings, Export.  
- **Gold Set + Scorer**: `tools/score_goldset.py` → P/R thresholds; regressions fail CI.  
- **Performance**: p95 ≤ 60s enforced in CI via timed baseline.

---

## 10) CI, Security, Conventions
- **CI**: workflows for backend (pytest) and frontend (build+tests).  
- **Pre‑commit**: ruff/black, eslint/prettier, type‑check.  
- **Conventional Commits**; PR template with story id + acceptance criteria checklist.  
- **git‑secrets**: block tokens/keys.  
- **CODEOWNERS**: `rules/`, `services/detection.py`, `reporting/` require review from Arch/QA.

---

## 11) Docs by Agents (Mary → Scrum)
- Put source docs in `docs/`:
  - `prd.md`, `architecture.md`, `uiux.md`, `po-validation.md`  
  - `stories/` contains the SM packets (1.1…5.2)  
- Shard PRD + Architecture with `*shard-doc`.  
- Keep “dev‑load‑always” list updated in agent prompts.

---

## 12) Runbooks (Windows)
- **Dev**: `scripts\ps\dev.ps1` (spawns API & Web)  
- **Tests**: `scripts\ps\test.ps1`  
- **Lint**: `scripts\ps\lint.ps1`

---

## 13) Legal & Copy
- **UI footer + export**: *Not legal advice* disclaimer.  
- **Privacy note**: LLM off by default; snippet‑only if enabled.  
- **Error copy**: use the provided codes/messages consistently.

---

## 14) Migration Worksheet (fill as you go)
- **Legacy repo URL/tag**: …  
- **Modules to assess**: extraction, detection, reporting, utils, data models.  
- **Candidates to port**: (list with evidence)  
- **Adapters needed**: (list)  
- **Decision**: keep/port/drop — owner & due date.

---

## 15) Risks & Mitigations
- **Scope creep** → PO lock + one‑story PRs.  
- **Legacy coupling** → adapter harness, quarantine folder.  
- **Performance regressions** → CI time gates + metrics wall.  
- **False greens** → broaden red‑flags; add hard negatives; QA review.  
- **Cost drift** → token caps + ledger; LLM off.

---

### Appendix A — PR Template
```
## Story
- ID: <epic.story>
- Acceptance Criteria: (paste from story packet)

## Changes
- Files touched

## Tests
- Unit:
- Integration:
- E2E:

## Screenshots / Evidence

## Checklist
- [ ] All acceptance criteria met
- [ ] New/updated tests added
- [ ] Lint/format clean
- [ ] No secrets added
```

### Appendix B — .gitignore highlights
```
.env
apps/api/.data/
__pycache__/
node_modules/
playwright-report/
```

### Appendix C — .editorconfig
```
root = true
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
indent_style = space
indent_size = 2
```

---

**You now have a clean start for Blackletter 3.0 plus a controlled plan to mine the old repo.** Execute Sprint A today; schedule the legacy inventory in parallel but keep production paths green and simple.

