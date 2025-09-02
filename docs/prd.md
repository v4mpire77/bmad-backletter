# Product Requirements Document

## Vision
Reduce GDPR-focused contract review from hours to minutes by producing evidence-backed findings with deterministic detection and optional LLM reasoning.

## Users & Personas
- **DPO / Compliance Officer** – manages rulepacks, reviews all analyses.
- **In-house Counsel / Solicitor** – uploads contracts, reviews findings, exports reports.
- **Org Owner / Admin** – manages billing, retention, SSO, and team access.
- **Paralegal** – uploads documents and reviews assigned matters.

## Scope
- Single-tenant per organisation with RBAC roles.
- Upload PDF/DOCX, run detection pipeline, view findings with evidence, export reports.
- Rulepack management for enabling/disabling rules and severities.
- Vector & keyword search across analyses.
- No offline mode, redlining, or non-GDPR jurisdictions.

## KPIs
- End-to-end analysis latency p95 ≤ 60s for 40-page PDFs.
- At least one finding surfaced with evidence window in MVP.
- 8 Article 28 obligation checks in first release.

## Epics
1. **E0 Baseline** – repo scaffold, CI, deterministic rule runner.
2. **E1 Ingestion** – upload, storage, text extraction, chunking.
3. **E2 Detection** – rulepacks, weak language lexicon, LLM reasoning.
4. **E3 Findings UI** – findings table, evidence drawer, export.

## Acceptance Criteria
- Uploading a valid PDF triggers an analysis job and surfaces at least one finding with clickable evidence window in ≤60s p95.
- Every finding includes verdict, severity, rationale, anchors[{text,page,offset}], evidence_window.
- Org-scoped RBAC prevents cross-tenant access.
- Admin can toggle a rulepack and impact next analysis.
- Stripe subscription change updates seat entitlements within 1 minute.
- Audit log export reproduces complete per-document trace.
