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

## Epic E4: Metrics, Logging & Observability

### Story E4.1: Instrument Metrics

- Capture latency, cost, and token counts; expose health and status endpoints.

### Story E4.2: Structured Logs & Dashboards

- Emit JSON logs and surface basic dashboards showing %LLM invocation.

## Epic E5: Templates, Clause Library & Interview Builder

### Story E5.1: Template Packs

- Load template packs with governed tone and conditional fields.

### Story E5.2: Guided Interview Flow

- Convert answers into documents using clause snippets and an interview-style UI.

## Epic E6: Governance & Settings

### Story E6.1: Compliance Modes

- Provide LLM kill-switch, OCR opt-in, and evidence-window configuration.

### Story E6.2: Retention Policies

- Allow org defaults and guardrails for data retention and deletion.

## Epic E7: Accounts, Auth & Roles

### Story E7.1: Authentication & Roles

- Email/password sign-in with Admin and Reviewer roles scoped to orgs.

### Story E7.2: Org Management

- Support org switching and basic admin screens.

## Epic E8: Evidence, Provenance & Review Controls

### Story E8.1: Review Workflow

- Track per-finding review status with override notes.

### Story E8.2: Provenance Trail

- Generate checksum manifests and "why" explainers for findings.

## Epic E9: Export, Sharing & Presentation

### Story E9.1: Themed Reports

- Apply report theming with red/amber/green mapping and watermarking.

### Story E9.2: Sharing & Data Exports

- Create shareable links (signed URLs) and CSV/JSON exports.

## Epic E10: Storage & Data Layer

### Story E10.1: Persistence Layer

- Provide SQLite-to-Postgres migration path and S3-compatible blob storage.

### Story E10.2: Maintenance Jobs

- Schedule backups and pruning/retention jobs with migrations.

## Epic E11: Evaluation & QA Harness

### Story E11.1: Gold Set & Labels

- Establish gold dataset with label schema and regression suite.

### Story E11.2: Detector Tests

- Add precision/recall gates with unit tests and fixtures.

## Epic E12: Cost & Performance Controls

### Story E12.1: Optimisation Layer

- Implement caching, batching, and concurrency limits with p95 budgets.

### Story E12.2: Token Safeguards

- Enforce token budgets per document and downgrade to `needs_review` on overflow.

## Epic E13: DevEx Tooling & Agent Flows

### Story E13.1: Developer Tools

- Provide CLI prompts, repo maps, scaffolds, and smoke scripts.

### Story E13.2: PR Workflow

- Supply seeded demo data plus PR templates and checklists.

## Epic E14: Integrations

### Story E14.1: Inbound Integrations

- Support email-in ingestion and DMS/SharePoint hooks.

### Story E14.2: Outbound & Crypto Prep

- Offer webhook callbacks and wallet/KMS adapter preparation.

## Epic E15: Pricing, Plans & Billing

### Story E15.1: Plan & Billing Engine

- Define plans, quotas, seat/usage toggles, and Stripe wiring.

### Story E15.2: Upgrade Flow

- Surface limits in the UI with trial and upgrade flows.

## Epic E16: Token & Evidence Layer

### Story E16.1: Signature Capture

- Capture wallet signatures and maintain doc-hash manifests.

### Story E16.2: Evidence Viewer

- Provide optional on-chain notarisation with revocation registry and viewer.
