# Project Brief: Blackletter 3.0

## Executive Summary

Blackletter 3.0 is a ground-up rebuild of a GDPR compliance checking tool, specifically focused on analyzing Data Processing Agreements (DPAs) against Article 28(3) requirements. The primary problem is the unreliable, thrashing state of the current legacy codebase, which hinders development and confidence. The target market includes legal professionals and compliance officers in firms or organizations handling EU data. The key value proposition is delivering a clean, deterministic, and explainable MVP built using a structured, agent-coordinated development process (BMAD V4) to ensure quality and maintainability from the outset.

## Problem Statement

The current legacy Blackletter repository is in a state of disarray, causing significant development thrash, mystery regressions, and hindering progress. This messy state impacts productivity, code quality, and the team's ability to deliver reliable features confidently. The problem has a high urgency as it prevents the team from effectively building upon or improving the existing tool. Existing attempts to work within the legacy codebase have proven insufficient, necessitating a clean-slate approach.

## Proposed Solution

The proposed solution is to create a new, clean repository for Blackletter 3.0, treating the old repo as a read-only artifact mine. The core concept is to build the Minimum Viable Product (MVP) using the BMAD V4 methodology, which involves structured documentation (PRD, Architecture), agent roles (PM, PO, SM, Dev, QA), and a defined story-based workflow. This solution succeeds by prioritizing simplicity, determinism, and clear documentation over premature complexity, ensuring a solid foundation. The high-level vision is a reliable, evidence-first GDPR checker that is easy to understand, extend, and maintain.

## Target Users

### Primary User Segment: Legal Professionals & Compliance Officers

These users are typically lawyers, legal analysts, or compliance managers working within law firms, corporations, or organizations that handle personal data processing under GDPR. Their current workflows often involve manually reviewing contracts or using disparate tools. Their specific needs include a reliable tool to quickly identify potential GDPR compliance risks in DPAs. Their primary goal is to efficiently and accurately assess Article 28(3) compliance to advise clients or ensure organizational adherence.

## Goals & Success Metrics

### Business Objectives

- Deliver a stable Blackletter 3.0 MVP within 2 sprints.
- Reduce development thrash and increase codebase confidence compared to the legacy version.
- Establish a scalable and maintainable architecture for future enhancements.

### User Success Metrics

- Ability to upload a PDF/DOCX DPA and receive a structured analysis of findings.
- Clear presentation of evidence snippets and rationale for each finding.
- Successful export of analysis reports in PDF/HTML format.

### Key Performance Indicators (KPIs)

- **MVP Delivery Time:** Complete Sprint A (Foundations) and Sprint B (UX & Ops) on schedule.
- **Codebase Health:** Pass all unit, integration, and E2E tests with defined quality gates (e.g., Precision ≥ 0.85, Recall ≥ 0.90).
- **Agent Workflow Efficiency:** Smooth handoff and status progression through PM/PO/SM/Dev/QA roles.

## MVP Scope

### Core Features (Must Have)

- **Document Ingestion:** Upload PDF/DOCX contracts (≤10MB) with validation (Story 1.1).
- **Text Extraction & Indexing:** Extract text, create page maps, and build sentence indices (Story 1.2).
- **Evidence Windows:** Build context windows around findings (±2 sentences) (Story 1.3).
- **Rulepack Loading:** Load and validate the core GDPR Article 28 rulepack (`art28_v1.yaml`) (Story 2.1).
- **Core Detection Engine:** Run rules against evidence windows to produce findings (verdict, snippet, rationale) (Story 2.2).
- **Findings UI:** Display analysis findings in a table with filtering/search and an evidence drawer (Story 3.1).
- **Report Export:** Export findings to PDF/HTML reports (Story 3.2).
- **Basic Token Ledger:** Track and enforce configurable token caps for LLM usage (Story 2.4).
- **Metrics Dashboard:** Display key operational metrics (latency, tokens, coverage) (Stories 4.1, 4.2).
- **Org Settings & Auth:** Configure LLM/OCR toggles and implement minimal role-based access (Stories 5.1, 5.2).

### Out of Scope for MVP

- Default OCR processing (off by default).
- Complex RAG or LLM features beyond token capping.
- Multi-tenancy beyond basic org-level settings.
- Advanced asynchronous job queues (Celery/Redis - Phase 2).
- Full Postgres database (using SQLite for dev - Postgres in Phase 2).

### MVP Success Criteria

The MVP is successful when users can upload a DPA, the system processes it using deterministic rules, presents findings with clear evidence in the UI, and allows exporting a report, all while meeting the defined performance and quality gates.

## Post-MVP Vision

### Phase 2 Features

- Migrate to durable async jobs (Celery/Redis).
- Transition to a production-grade database (Postgres).
- Enhance authentication (SSO).
- Potentially introduce scoped RAG capabilities.
- Expand rule coverage beyond Article 28.

### Long-term Vision

Become the go-to, highly accurate and explainable tool for automated GDPR (and potentially other regulatory) compliance checking, trusted by legal professionals globally.

### Expansion Opportunities

- Support for other regulatory frameworks (e.g., CCPA, HIPAA).
- Multi-language document analysis.
- Integration with broader legal tech ecosystems or CLM tools.

## Technical Considerations

### Platform Requirements

- **Target Platforms:** Web application (Chrome, Firefox, Edge latest versions).
- **Browser/OS Support:** Modern browsers on Windows, macOS, Linux.
- **Performance Requirements:** p95 document processing latency ≤ 60s; Cost ≤ £0.10/doc.

### Technology Preferences

- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui.
- **Backend:** FastAPI (Python 3.11), Uvicorn.
- **Database:** SQLite (dev), Postgres (Phase 2).
- **Hosting/Infrastructure:** Render (Docker), with potential migration to cloud providers (Phase 2).

### Architecture Considerations

- **Repository Structure:** Monorepo with `apps/web` and `apps/api`.
- **Service Architecture:** Thin FastAPI service with modular `services/` (extraction, detection, reporting).
- **Integration Requirements:** None critical for MVP.
- **Security/Compliance:** Disable LLM by default; snippet-only processing if enabled; PII redaction.

## Constraints & Assumptions

### Constraints

- **Budget:** Limited, favoring open-source tools and simple hosting.
- **Timeline:** Strict 2-sprint MVP delivery plan.
- **Resources:** Small, cross-functional team leveraging AI agents.
- **Technical:** Must use Windows-friendly development tools.

### Key Assumptions

- The BMAD V4 process will effectively coordinate agent roles and workflow.
- Developers can successfully implement stories based on the provided specifications and 'dev-load-always' files.
- The core rulepack (`art28_v1.yaml`) provides sufficient deterministic coverage for an MVP.
- Users understand this is an MVP with limited scope.

## Risks & Open Questions

### Key Risks

- **Scope Creep:** Risk of adding features beyond the strict MVP during development. *Mitigation:* PO lock and one-story PRs.
- **Legacy Coupling:** Risk of accidentally reintroducing complexity from the old codebase. *Mitigation:* Adapter harness, strict review.
- **Performance Regressions:** Risk of the new system being slower or more expensive than desired. *Mitigation:* CI time gates, metrics wall.

### Open Questions

- How will the final UI/UX details be refined beyond the architectural guidelines?
- What specific strategies will be used for migrating valuable components from the legacy repo in Phase 2?

### Areas Needing Further Research

- Detailed performance profiling and optimization if initial gates are not met.
- User feedback mechanisms and potential impact analysis for future expansions.

## Next Steps

### Immediate Actions

1.  Finalize the clean `blackletter/` repository structure.
2.  Shards the core PRD and Architecture documents into the `docs/` folder.
3.  Scrum Master begins facilitating the story development cycle starting with Story 1.1.

### PM Handoff

This Project Brief provides the full context for Blackletter 3.0. The next step is to proceed with the detailed PRD creation, ensuring alignment with this brief. The development cycle, guided by the Scrum Master, Product Owner, and QA, will then implement the stories sequentially.