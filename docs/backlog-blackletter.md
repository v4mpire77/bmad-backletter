# Blackletter — Backlog & Epics (shard)

This shard contains the Epics, Stories, and initial acceptance criteria for the MVP.


## Epic E0: Platform & Security Baseline

**Epic Goal:** Establish foundational infrastructure, security protocols, and developer workflows.

### Story E0.1: Repository Scaffold & Source Tree

- Create monorepo with `apps/web` (Next.js) and `apps/api` (FastAPI).
- Include `docs/`, `tools/windows/`, and `core-config.yaml`.

### Story E0.2: Windows Developer Environment

- PowerShell runbooks (`dev.ps1`, `test.ps1`) that spin up docker-compose and run tests.

### Story E0.3: Coding Standards & Linters

- Configure ruff, black, ESLint, and Prettier; add CI job to enforce.

## Epic E1: Ingestion & Extraction

### Story E1.1: Upload & Job Orchestration

- POST `/contracts` accepts PDF/DOCX up to 10MB; returns `job_id` and job status endpoint.

### Story E1.2: Text Extraction

- Extract text, page map, and sentence index; store artifacts and link to analysis records.

### Story E1.3: Evidence Window Builder

- Build ±2 sentence evidence windows and handle page boundaries.

## Epic E2: GDPR Rule Engine & Detection

### Story E2.1: Rule Pack Loader

- YAML-based rule packs with versioning and validation.

### Story E2.2: Obligation Detector Runner

- Deterministic rule execution producing verdicts and evidence snippets.

## Epic E3: Findings & Report UI

### Story E3.1: Findings Table

- Display 8 obligations with verdicts, snippets, and filters.

### Story E3.2: Evidence Drawer

- Click to open detailed evidence with rule ID and copy action.

### Story E3.3: Export Report

- Generate self-contained HTML and PDF reports reproducing findings.
