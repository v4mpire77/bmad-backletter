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
