# Blackletter GDPR Contract Analyzer — Product Requirements Document (PRD)

**Project:** Blackletter (GDPR Vendor Contract Checker)

**Owner (PM):** John (BMad Agent)

**Version:** v2.0 (Consolidated)

**Date:** 2025-09-01

**Intended Readers:** Analyst (Mary), Architect (Winston), PO (Sarah), SM (Michael), Dev, QA

---

## 1. Vision & Goals

**Vision:** To shrink the time required for vendor-contract GDPR review from hours to minutes using explainable, deterministic checks against GDPR Article 28(3), with every finding backed by pinpoint citations and clear, auditable rationale.

**Primary Goals (MVP):**
- Deliver 8 core obligation checks derived from GDPR Art. 28(3)(a)–(h) with clear verdicts: Pass / Weak / Missing / Needs Review.
- Provide evidence-first results, showing the "why" for every finding with the specific rule ID, contract snippet, and location.
- Generate an exportable HTML/PDF report suitable for sharing with internal stakeholders and external vendors.
- Operate with low cost and tight latency (under 60 seconds for a typical 10-page document) at an initial small scale.

**Non‑Goals (MVP):**
- Automated contract redlining or clause rewriting.
- Compliance checks for jurisdictions beyond UK/EU GDPR.
- Batch processing, real-time collaboration features, or complex workflow automation.

## 2. Users & Personas

- **DPO / Data Protection Lead (Primary):** Needs fast, evidence-backed clause checks to accelerate vendor reviews and ensure compliance.
- **In-house Counsel:** Wants a consistent, defensible screening tool to triage contracts before engaging in deep legal analysis.
- **External Solicitor:** Requires a tool for quick triage that produces a clean, client-friendly report.
- **SME Founder/Ops:** Needs a sanity check on vendor Data Processing Agreements (DPAs) during procurement without requiring deep legal expertise.

**Top Jobs‑to‑be‑Done:**
- Upload a vendor contract (PDF/DOCX) and receive a clear, cited pass/weak/missing summary of the eight core Art. 28(3) obligations.
- Drill down into the exact contract snippets and rule rationales to confirm or challenge a finding.
- Export a professional, shareable report for internal records or stakeholder communication.

## 3. Scope (MVP)

### In‑Scope Functionalities
- **File Ingestion:** Securely upload PDF and DOCX files up to 10MB via a web interface, managed by an asynchronous job queue.
- **Text Extraction & Indexing:** Accurately extract text and map it to page numbers and sentence indices. OCR is an optional feature, disabled by default.
- **Rule‑Driven Detection:** Execute the art28_v1 rulepack deterministically across the indexed text to compute verdicts for each of the 8 core GDPR obligations.
- **Findings UI:** A clear, intuitive web interface displaying findings with color-coded verdicts (Red/Amber/Green), filters, and a detailed evidence drawer.
- **Report Export:** Generate a self-contained HTML/PDF report containing document metadata, a findings summary, and detailed evidence for each clause.
- **History:** A per-organization view listing all prior contract analyses with basic metadata and a link to the full report.
- **Settings:** An admin panel to toggle features like the LLM provider (default is none), OCR, and set data retention policies.

### Out of Scope (MVP)
- Redline suggestions, vendor-to-vendor contract comparisons, or cross-document diffing.
- Analysis of multi-language contracts or deep PII discovery within the text.
- SSO and granular Role-Based Access Control (RBAC) beyond a simple Admin/Reviewer model.

## 4. Quality Attributes & KPIs

- **Latency:** p95 ≤ 60 seconds for end-to-end processing of a document up to 10MB.
- **Cost:** ≤ £0.10 per document at default settings, with a visible token ledger for any LLM-assisted features.
- **Accuracy:** Precision ≥ 0.85 and Recall ≥ 0.90 on the internal Gold Set v1 of test documents.
- **Explainability:** ≥ 95% of all findings must include a contract snippet and a clear rule ID.
- **Coverage:** No undetected topics among the eight core detectors for a fully compliant DPA.

## 5. Constraints & Assumptions

- **Determinism First:** The core analysis engine will rely on deterministic methods (regex, lexicons, rules) with ML/LLM features being strictly opt-in and off by default.
- **Windows-friendly Development:** The development environment and scripts must be fully functional on Windows.
- **Evidence Window:** The default context window for evidence snippets is ±2 sentences, configurable per detector.
- **Verdicts:** The system will default to conservative verdicts (e.g., "Needs Review") when ambiguity is high.

## 6. Acceptance Wordings (Analyst-Defined)

| Detector | Must‑Include (Anchors) | Weak Cues | Red‑Flags |
|---|---|---|---|
| (a) Instructions | only on documented/written instructions; lawful carve‑out notice | commercially reasonable; where practicable; endeavour | provider discretion; subject to provider policies |
| (b) Confidentiality | authorised persons; confidentiality obligation | industry standard; reasonable efforts | where feasible only; business purposes exception |
| (c) Security (Art. 32) | technical and organisational measures; Article 32 | commercially reasonable security; industry standard | subject to change without notice |
| (d) Sub‑processors | prior authorisation/notice; flow‑down equivalence | materially similar; post‑hoc notice | unrestricted appointment; terminate‑only |
| (e) DSAR Assist | assist controller under Arts. 12–23 | reasonable efforts | assistance at sole discretion; paid consulting only |
| (f) Breach Notice | notify without undue delay | as soon as practicable; within a reasonable time | internal threshold required; no timing promise |
| (g) Return/Delete | delete or return at end; delete copies | periodically delete | retain by default for analytics |
| (h) Audits/Info | make available info; allow & contribute to audits | subject to provider policies; attestations‑only | audits disallowed; SOC2‑only regardless of scope |

## 7. Epics & Story Map (MVP)

### Epic E0: Platform & Security Baseline
**Epic Goal:** To establish the foundational infrastructure, security protocols, and development environment for the project, ensuring a stable and secure platform for all future work.

#### Story E0.1: Repository Scaffold & Source Tree
**As a** developer, I want a project repository with a well-defined structure, so that I can easily find and manage code and documentation.

**Acceptance Criteria:**
- A monorepo is created with apps/web (Next.js 14, TS 5) and apps/api (FastAPI 0.111, Python 3.11).
- The repository includes docs/, scripts/ps/, and a core-config.yaml.
- PowerShell runbooks (dev.ps1, test.ps1, lint.ps1) must run successfully on Windows.

#### Story E0.2: Windows Developer Environment
**As a** developer, I want to set up my local environment on Windows easily, so that I can start contributing to the project quickly.

**Acceptance Criteria:**
- The local setup uses py -3.11 and npm ci.
- No Bash-only scripts are used in the setup process.
- Documentation is updated with clear installation and run steps for Windows developers.

#### Story E0.3: Coding Standards & Linters
**As a** developer, I want clear coding standards to be enforced automatically, so that the codebase remains consistent and high-quality.

**Acceptance Criteria:**
- Backend: ruff and black are configured for linting and formatting.
- Frontend: ESLint and Prettier are configured for formatting and style.
- A CI job is configured to enforce linting and testing, blocking merges for non-compliant code.

### Epic E1: Ingestion & Extraction
**Epic Goal:** To enable users to upload contract files, which the service will then process into structured, analyzable text with a corresponding page map and sentence index.

#### Story E1.1: Upload & Job Orchestration
**As a** user, I want to upload a contract file to the system, so that the analysis process can begin.

**Acceptance Criteria:**
- POST /contracts accepts PDF/DOCX files up to 10MB.
- The API returns a job_id, and GET /jobs/{id} returns the job's status (queued | running | done | error).
- Upon successful upload, a new analysis record is created with the filename, size, and timestamp.

#### Story E1.2: Text Extraction (PDF/DOCX)
**As a** system, I want to accurately extract all text from an uploaded document, so that it can be used for rule-driven detection.

**Acceptance Criteria:**
- The system can extract text, a page map (mapping pages to character ranges), and a sentence index from both PDF and DOCX files.
- Extracted artifacts are stored and linked to the correct analysis record.
- Malformed or corrupt documents are handled gracefully with explicit error codes in the job status.

#### Story E1.3: Evidence Window Builder
**As a** system, I want to generate a text snippet with surrounding context for any finding, so that users can see the evidence for a rule match.

**Acceptance Criteria:**
- Given a character span, the system returns a snippet containing the matched text plus a ±2 sentence window.
- The size of the evidence window is configurable per detector.
- The function correctly handles boundaries and does not leak content across pages.

### Epic E2: GDPR Rule Engine & Detection (Art. 28(3))
**Epic Goal:** To build a deterministic rules engine that checks contracts against the 8 core GDPR Article 28(3) obligations and produces clear, evidence-backed verdicts.

#### Story E2.1: Rule Pack Loader
**As a** system, I want to load versioned rule packs, so that I can perform deterministic compliance checks.

**Acceptance Criteria:**
- Rule packs are defined in YAML files with unique IDs and version numbers.
- The system validates the YAML syntax of a rule pack before loading it.
- The active rule pack is configurable via an environment variable.

#### Story E2.2: Obligation Detector Runner
**As a** system, I want to check each clause for GDPR obligations, so that I can classify its compliance level.

**Acceptance Criteria:**
- Each of the 8 GDPR obligations is represented as a deterministic rule in the art28_v1 rulepack.
- The rules run against the sentence index produced in Epic 1.
- The output for each rule is a verdict: Pass, Weak, Missing, or Needs Review, complete with the evidence snippet.

### Epic E3: Findings & Report UI
**Epic Goal:** To provide users with a clear and intuitive user interface for reviewing findings, exploring evidence, and exporting compliance reports.

#### Story E3.1: Findings Table
**As a** user, I want a central findings table, so that I can quickly see the compliance status of my contract.

**Acceptance Criteria:**
- A table on the document page lists the 8 GDPR obligations.
- Each row displays the verdict with a corresponding color code (Red/Amber/Green), a short rationale, and the evidence snippet.
- The table can be filtered by verdict status.

#### Story E3.2: Evidence Drawer
**As a** user, I want to drill down into a finding, so that I can view the supporting evidence from the contract.

**Acceptance Criteria:**
- Clicking a finding row opens a detail drawer/panel.
- The drawer displays the full evidence snippet, the rule ID, and the detailed rationale text.
- The drawer includes a button to easily copy the evidence text.

#### Story E3.3: Export Report (PDF/HTML)
**As a** user, I want to export the findings, so that I can share the compliance results with stakeholders.

**Acceptance Criteria:**
- The application can generate and download a report in both PDF and HTML formats.
- The report reproduces the findings table, including verdicts, snippets, and document metadata.
- The exported file is self-contained and easily shareable.

### Epic E4: Metrics, Logging & Observability
**Epic Goal:** To instrument the system with metrics and logs that expose health, cost, and usage for operators.

#### Story E4.1: Instrument Metrics
**As a** developer, I want latency, cost, and token metrics emitted, so that I can monitor system performance.

**Acceptance Criteria:**
- Metrics capture request latency, token usage, and %LLM invocation.
- A `/health` endpoint reports service status.
- Metrics are exposed for scraping (e.g., Prometheus format).

#### Story E4.2: Structured Logs & Dashboards
**As a** operator, I want structured JSON logs and basic dashboards, so that I can trace issues quickly.

**Acceptance Criteria:**
- Logs are structured JSON including request IDs and verdict outcomes.
- A minimal dashboard visualises error rates and token spend.
- Logging level is configurable per environment.

### Epic E5: Templates, Clause Library & Interview Builder
**Epic Goal:** To help users generate documents via reusable templates and guided interviews.

#### Story E5.1: Template Packs
**As a** content admin, I want template packs with governed tone and conditional fields, so that documents are consistent.

**Acceptance Criteria:**
- Template packs are versioned and selectable at document creation.
- Fields can be marked conditional with default microcopy.
- Template metadata enforces approved tone guidelines.

#### Story E5.2: Guided Interview Flow
**As a** user, I want a guided interview that outputs a document, so that I can assemble contracts without legal expertise.

**Acceptance Criteria:**
- Interview prompts map to clause snippets.
- Completed interviews generate a draft document in the editor.
- Users can revisit and edit previous answers.

### Epic E6: Governance & Settings (Compliance Modes)
**Epic Goal:** To provide organisational controls over LLM usage, retention, and evidence handling.

#### Story E6.1: Compliance Modes
**As a** admin, I want switches for LLM usage, OCR opt-in, and evidence windows, so that I can enforce policy.

**Acceptance Criteria:**
- Admin UI toggles LLM kill-switch and snippet-only mode.
- OCR processing requires explicit opt-in.
- Evidence window size is configurable per org.

#### Story E6.2: Retention Policies
**As a** admin, I want to set data retention defaults, so that stored artifacts comply with policy.

**Acceptance Criteria:**
- Retention duration is configurable per organisation.
- Expired artifacts are pruned automatically.
- Default org settings apply to new projects.

### Epic E7: Accounts, Auth & Roles / Multi-Tenancy
**Epic Goal:** To authenticate users and scope access by organisation with basic admin capabilities.

#### Story E7.1: Authentication & Roles
**As a** user, I want email/password sign-in with Admin and Reviewer roles, so that access is controlled.

**Acceptance Criteria:**
- Users can register and login with email and password.
- Roles determine access to admin features vs. review-only.
- Sessions are scoped to a single organisation.

#### Story E7.2: Org Management
**As a** admin, I want to switch organisations and manage members, so that multi-tenant use is supported.

**Acceptance Criteria:**
- An org switcher is available in the UI.
- Admin screens list members and roles.
- Org-scoped API keys can be rotated.

### Epic E8: Evidence, Provenance & Review Controls
**Epic Goal:** To track review status and provenance of findings for auditability.

#### Story E8.1: Review Workflow
**As a** reviewer, I want to mark findings reviewed and add notes, so that decisions are auditable.

**Acceptance Criteria:**
- Findings support statuses: pending, approved, rejected.
- Override notes are logged with timestamp and user.
- Review status affects export output.

#### Story E8.2: Provenance Trail
**As a** auditor, I want checksums and provenance manifests, so that evidence integrity is verifiable.

**Acceptance Criteria:**
- Each finding has a checksum of the evidence snippet.
- A manifest records source document hash and processing steps.
- A “why” explainer shows rule logic that led to the finding.

### Epic E9: Export, Sharing & Presentation
**Epic Goal:** To allow sharing of results with custom theming and data exports.

#### Story E9.1: Themed Reports
**As a** user, I want themed reports with RAG mapping, so that presentations match organisation style.

**Acceptance Criteria:**
- Reports support custom colour themes and watermarking.
- Red/amber/green verdict colours map to org palette.
- Theme selection persists per export.

#### Story E9.2: Sharing & Data Exports
**As a** user, I want shareable links and data exports, so that stakeholders can review findings offline.

**Acceptance Criteria:**
- Shareable links use signed URLs with expiry.
- Findings can be exported as CSV or JSON.
- Exported data excludes unreleased drafts.

### Epic E10: Storage & Data Layer
**Epic Goal:** To build a scalable persistence layer with backups and retention jobs.

#### Story E10.1: Persistence Layer
**As a** engineer, I want a path from SQLite to Postgres with blob storage, so that the system can scale.

**Acceptance Criteria:**
- Database migrations support both SQLite and Postgres.
- Binary artifacts are stored in an S3-compatible bucket.
- Connection strings are configured via environment variables.

#### Story E10.2: Maintenance Jobs
**As a** operator, I want automated backups and pruning, so that data is durable and compliant.

**Acceptance Criteria:**
- Nightly backups are stored in a separate bucket.
- Retention jobs purge expired data.
- Migrations are idempotent and logged.

### Epic E11: Evaluation & QA Harness
**Epic Goal:** To ensure detector accuracy via labelled datasets and regression tests.

#### Story E11.1: Gold Set & Labels
**As a** QA engineer, I want a labelled gold dataset, so that detector performance can be measured.

**Acceptance Criteria:**
- Gold set v1 with label schema is stored under `docs/`.
- Precision and recall are calculated for each rule.
- Regression suite runs against the gold set.

#### Story E11.2: Detector Tests
**As a** developer, I want unit tests and fixtures, so that detectors are reliable.

**Acceptance Criteria:**
- Each detector has unit tests covering edge cases.
- Fixtures are synthetic and versioned.
- CI fails if precision/recall drop below thresholds.

### Epic E12: Cost & Performance Controls
**Epic Goal:** To keep operations within budget through caching and token management.

#### Story E12.1: Optimisation Layer
**As a** engineer, I want caching and batching, so that throughput meets p95 latency goals.

**Acceptance Criteria:**
- Caching layer stores repeat analysis results.
- Batching combines small jobs into single runs.
- Concurrency limits are configurable.

#### Story E12.2: Token Safeguards
**As a** system, I want token budgets, so that excessive usage degrades gracefully.

**Acceptance Criteria:**
- Token budget per document is configurable.
- Overages downgrade verdicts to `needs_review` and skip LLM calls.
- Metrics log token consumption per job.

### Epic E13: DevEx Tooling & Agent Flows
**Epic Goal:** To streamline developer workflows with tooling and predefined agent paths.

#### Story E13.1: Developer Tools
**As a** developer, I want CLI prompts, repo maps, and scaffolds, so that onboarding is faster.

**Acceptance Criteria:**
- CLI provides commands for common tasks (lint, test, scaffold).
- Repo map outlines key modules and stories.
- Smoke scripts validate environment setup.

#### Story E13.2: PR Workflow
**As a** contributor, I want seeded demo data and PR templates, so that changes are easy to review.

**Acceptance Criteria:**
- Demo data script seeds sample contracts.
- PR templates include checklists per area.
- Instructions reference CODEOWNERS for review routing.

### Epic E14: Integrations
**Epic Goal:** To connect with external systems for ingest and notifications.

#### Story E14.1: Inbound Integrations
**As a** user, I want email-in and DMS hooks, so that documents flow in from existing systems.

**Acceptance Criteria:**
- Emails forwarded to a special address create new uploads.
- SharePoint/DMS connectors fetch documents via API.
- Errors are logged with correlation IDs.

#### Story E14.2: Outbound & Crypto Prep
**As a** developer, I want webhook callbacks and wallet/KMS adapters, so that external systems can react and sign data.

**Acceptance Criteria:**
- Webhooks fire on job completion and finding approval.
- Wallet/KMS adapter scaffolding is in place for E16.
- Integration endpoints are documented.

### Epic E15: Pricing, Plans & Billing (Commercialisation)
**Epic Goal:** To monetise the service with plans, quotas, and billing flows.

#### Story E15.1: Plan & Billing Engine
**As a** product manager, I want plan tiers with quotas, so that usage can be monetised.

**Acceptance Criteria:**
- Plans define seat counts and usage limits.
- Stripe integration charges and tracks usage.
- Over-limit usage prompts upgrade.

#### Story E15.2: Upgrade Flow
**As a** user, I want trial and upgrade flows surfaced in the UI, so that I can convert easily.

**Acceptance Criteria:**
- Trial accounts show remaining quota in the UI.
- Upgrade modal links to billing portal.
- Downgrades warn about exceeded limits.

### Epic E16: Token/Blockchain Signature & Evidence Layer (Pilot)
**Epic Goal:** To capture cryptographic evidence of documents and make it verifiable.

#### Story E16.1: Signature Capture
**As a** user, I want to sign document hashes with my wallet, so that provenance is verifiable.

**Acceptance Criteria:**
- Wallet signatures are stored alongside doc-hash manifests.
- Revocation registry records invalidated signatures.
- Signature capture is optional per document.

#### Story E16.2: Evidence Viewer
**As a** reviewer, I want an evidence viewer with on-chain notarisation, so that authenticity can be inspected.

**Acceptance Criteria:**
- Viewer displays signature status and blockchain transaction.
- On-chain notarisation is configurable per org.
- Evidence viewer links from each finding.

## 8. Definition of Ready / Done

**Definition of Ready (for stories):** Acceptance criteria are written and testable; any UX implications are defined; all dependencies are listed.

**Definition of Done (for stories):** All unit and integration tests pass; acceptance criteria are demonstrated and verified; QA review is complete and recorded; any relevant metrics are updated; a documentation snippet has been added if necessary.

## 9. Dependencies & Risks

- **Extraction Variance:** The parsing of PDF and DOCX files can be inconsistent. Mitigation: Use robust, well-maintained libraries and implement graceful error handling.
- **Clause Phrasing Variance:** The language used in contracts varies widely. Mitigation: Use a combination of a rulepack and a weak-language lexicon, with plans for a small ML model for triage in a later phase.
- **Token Cost Drift:** If/when LLMs are used, costs can be unpredictable. Mitigation: Implement strict token caps and keep the LLM provider disabled by default.

## 10. Release Plan (MVP)

**Milestone A:** Epics 1–2 are complete. The system can ingest a document and run the rule engine against it, with a successful smoke test on 3 gold-standard documents.

**Milestone B:** The basic UI and export functionality (Stories 3.1–3.2) are complete, along with foundational metrics (Story 4.1).

**Milestone C:** The coverage meter (Story 4.2), settings panel (Story 5.1), and basic authentication (Story 5.2) are complete, freezing the MVP feature set.

## 11. Open Questions

- Which LLM provider (if any) should be exposed first when the feature is toggled on?
- What is the preferred PDF engine for exporting reports (e.g., wkhtmltopdf vs. headless Chromium)?
- Should we start with SQLite or Supabase Postgres for storing artifacts in the local development environment?

## 12. Appendices

- **A. Analyst Pack Reference:** Includes acceptance wordings, the weak-language lexicon, the rulepack skeleton, and the gold-set schema.
- **B. UX Specification:** front-end-spec.md
- **C. Architecture Document:** fullstack-architecture.md
