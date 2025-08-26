# Project Brief: GDPR Processor Obligations Checker

## Executive Summary

This project aims to develop a rules-first, cost-efficient "blackletter system" to automatically check GDPR processor agreements for compliance with Article 28(3) obligations. It solves the problem of manual, inconsistent, and time-consuming contract reviews for legal professionals, offering a transparent, auditable, and highly accurate solution that minimizes reliance on expensive LLM calls.

## Problem Statement

Legal professionals currently spend 2-6 hours manually reviewing each contract to ensure GDPR Article 28(3) compliance, leading to inconsistency, fatigue, and potential missed clauses. Existing "AI compliance" tools often lack transparency, are expensive, and provide black-box results without clear citations or evidence, leading to a lack of trust and auditability. The urgency stems from increasing regulatory scrutiny and the need for efficient, defensible compliance processes.

## Proposed Solution

Our solution is a rules-first GDPR processor-obligations checker that prioritizes deterministic analysis and minimizes LLM usage to keep costs near-zero. It will ingest PDF/DOCX contracts, extract relevant clauses, apply a curated YAML/regex rule engine, and use LLMs only for highly ambiguous or borderline cases. The system will output structured issues, a coverage map, and an auditable report with clause snippets and citations, ensuring transparency and verifiability.

## Target Users

### Primary User Segment: Small to Medium Law Firms & Solo Practitioners

*   **Demographic/firmographic profile:** Legal professionals in small to medium-sized law firms or solo practices, often handling a high volume of contracts with limited resources for extensive manual review.
*   **Current behaviors and workflows:** Manually reviewing contracts, often using checklists or prior experience, and spending significant time on each document. They value efficiency and accuracy but are highly cost-sensitive.
*   **Specific needs and pain points:** Need to ensure compliance without incurring high costs, desire for consistent and auditable results, struggle with the time commitment of manual reviews, and distrust black-box AI solutions.
*   **Goals they're trying to achieve:** Reduce review time, ensure GDPR compliance, maintain high accuracy, and provide defensible advice to clients.

### Secondary User Segment: In-house Legal Teams (SMEs)

*   **Demographic/firmographic profile:** Legal counsel within small to medium-sized enterprises (SMEs) who manage internal contracts and vendor agreements.
*   **Current behaviors and workflows:** Similar to law firms, they perform internal contract reviews but often have even tighter budget constraints and a need for rapid, reliable assessments.
*   **Specific needs and pain points:** Cost-effective compliance solutions, quick turnaround for contract approvals, and tools that integrate easily into their existing workflows.
*   **Goals they're trying to achieve:** Streamline internal compliance processes, reduce legal risk, and free up time for more strategic legal work.

## Goals & Success Metrics

### Business Objectives

*   Achieve a p95 latency of ≤ 60 seconds per document (local parse + selective LLM).
*   Maintain an average cost per document of ≤ £0.10.
*   Attain precision ≥ 0.85 and recall ≥ 0.90 on the gold set across all 8 detectors.

### User Success Metrics

*   Reduce manual contract review time by 60% or more.
*   Achieve "zero missed compliance flags" for GDPR Art. 28(3) obligations.
*   Maintain an explainability rate of ≥ 95% (findings include clause path + snippet).

### Key Performance Indicators (KPIs)

*   **p95 Latency:** Time taken for 95% of documents to be processed from upload to first signal.
*   **Cost per Document:** Average cost incurred per document processed, primarily driven by LLM token usage.
*   **Precision/Recall:** Standard metrics measured against a curated gold set of contracts.
*   **Explainability Rate:** Percentage of findings that include a clear clause location and snippet.
*   **Coverage:** Percentage of documents producing a pass/fail for each detector (no "unknown" gaps).
*   **Time-to-first-insight:** Time from document upload to the display of initial findings (target < 3 minutes).
*   **User Report Export Rate:** Percentage of users who export the generated compliance report.
*   **Weekly Returning Users:** Number of unique users engaging with the system on a weekly basis.

## MVP Scope

### Core Features (Must Have)

*   **PDF/DOCX Ingestion & Text Extraction:** Ability to upload and extract text from common contract formats.
*   **8 GDPR Art. 28(3) Detectors:** Implementation of the eight core checks (instructions, confidentiality, security, subprocessors, DSAR assistance, breach notification, deletion/return, audits/info).
*   **Rules-First Engine:** Deterministic YAML/regex rules to identify clear passes, weaknesses, or missing clauses.
*   **Snippet-Only LLM Integration (Gated):** LLM calls only for ambiguous cases, sending only small, relevant snippets, with a hard token cap.
*   **Evidence-First UI:** Display of findings with clause snippets, rule IDs, and clear verdicts (Pass/Weak/Missing/Needs Review).
*   **Coverage Meter:** Visual representation of detector coverage for the document.
*   **PDF Export:** One-click generation of a compliance report (HTML to PDF) including findings, snippets, and citations.
*   **Token & Latency Logger:** Live display of cost per document and processing time.
*   **Gold Set Evaluation:** Internal tooling to measure precision/recall against a curated gold set.
*   **Local SQLite Cache:** Caching of LLM responses for repeated prompts/snippets.
*   **Conservative Defaults:** Defaulting to "needs review" for low-confidence findings.

### Out of Scope for MVP

*   Full-fledged LLM generation (e.g., redlining, clause rewriting).
*   Batch processing of documents.
*   Cloud persistence of uploaded documents (default is ephemeral/local).
*   Advanced analytics dashboards beyond basic metrics.
*   Integrations with practice management systems.
*   Monetization features beyond a basic free offering.
*   Support for non-GDPR compliance checks.

### MVP Success Criteria

*   Achieve target KPIs (p95 latency ≤ 60s, avg cost ≤ £0.10, P ≥ 0.85 / R ≥ 0.90) on the gold set.
*   Demonstrate a clear reduction in manual review time for pilot users.
*   Receive positive feedback on transparency and auditability from legal professionals.

## Post-MVP Vision

### Phase 2 Features

*   Expand weak-language lexicon and refine existing rules.
*   Implement a local classifier for ambiguous triage (reducing LLM calls further).
*   Build a "metrics wall" and clause navigator in the UI.
*   Introduce a "Tight/Normal/Lenient" rule pack selection.
*   Develop a "Dispute" button for user feedback on findings.

### Long-term Vision

*   Autonomous Compliance Counsel (drafting opinions/clauses).
*   Real-time Contract Risk Monitoring + Breach Forecasting.
*   Regulatory Simulation Engine ("What-If Lab").
*   Legal-grade RAG & domain embeddings.
*   Fine-tuned legal LLMs.

### Expansion Opportunities

*   Vertical expansions into other legal domains (employment, property, financial services).
*   Localization for other EU states and international regulations.
*   Playbook marketplace for crowd-sourced templates.

## Technical Considerations

### Platform Requirements

*   **Target Platforms:** Windows (primary for MVP).
*   **Browser/OS Support:** Standard modern web browsers for UI (if any).
*   **Performance Requirements:** p95 latency ≤ 60s/doc.

### Technology Preferences

*   **Frontend:** Minimalist, potentially a simple web UI or local application.
*   **Backend:** Python (FastAPI) for core logic and API.
*   **Database:** SQLite for MVP (in-memory or local file-based cache/index).
*   **Hosting/Infrastructure:** Local/offline first; optional, rate-limited hosted demo later.

### Architecture Considerations

*   **Repository Structure:** Modular, with clear separation for `analyzer`, `api`, `rules`, `tests`, `docs`.
*   **Service Architecture:** Single-process HTTP app with optional background worker for batching.
*   **Integration Requirements:** Backend `contracts.py` review endpoint, dashboard issues table, CSV export.
*   **Security/Compliance:** Default to zero data retention, in-memory processing, local-only cache, snippet-only LLM calls, no PII to cloud LLMs.

## Constraints & Assumptions

### Constraints

*   **Budget:** Ideally free, with a hard cap of ≤ £0.10 per document for any external services.
*   **Timeline:** Rapid iteration, aiming for a functional MVP within 7 days.
*   **Resources:** Lean team, relying heavily on open-source tools and efficient development practices.
*   **Technical:** Windows-first development environment.

### Key Assumptions

*   Deterministic rules can cover a significant majority of compliance checks.
*   LLMs are primarily needed for nuanced interpretation of ambiguous clauses, not for core logic.
*   Users value transparency and auditability over black-box "AI magic."
*   A small, curated gold set is sufficient for initial evaluation and training.
*   The core value proposition (speed, consistency, explainability) will drive adoption even with a narrow scope.

## Risks & Open Questions

### Key Risks

*   **Clause Variance:** Rules may miss oblique phrasing in diverse contract templates.
*   **LLM Hallucination/Over-claim:** LLM summaries without quote-verification can invent coverage.
*   **Token Blow-ups:** Long documents + poor chunking = runaway costs.
*   **False Reassurance:** "Green" badge implies legal safety; users may over-rely without lawyer review.
*   **Data Handling:** Uploads may contain PII; retention, jurisdiction, and DPA with any third-party API matter.
*   **Free-tier Fragility:** Rate limits, cold starts, or policy changes can break workflows.

### Open Questions

*   What are the exact acceptance wordings for each Art. 28(3) duty to encode in rules/tests?
*   How will we expand the weak-language lexicon effectively without over-flagging?
*   What is the optimal final chunking strategy (header-aware + size limits) for real DPAs/MSAs?

### Areas Needing Further Research

*   Optimal embedding/storage choice for post-MVP (pgvector vs. in-memory).
*   Detailed LLM call budget plan: which cases *must* invoke LLM vs. use template text.
*   Strategies for continuous refinement of deterministic rules based on user feedback and new data.

## Appendices

### A. Research Summary

This Project Brief heavily leverages the insights from a comprehensive brainstorming session on "Building Blackletter Systems with Low/Free Costs." Key findings from that session, including detailed analyses from First Principles Thinking, Six Thinking Hats (White, Red, Black, Yellow, Green, Blue), Five Whys, and SCAMPER (Substitute, Combine, Adapt, Modify, Put to Another Use, Eliminate), have directly informed the problem statement, proposed solution, technical considerations, and risk assessment within this brief.

### B. Stakeholder Input

(No specific stakeholder input was gathered during this session, but this section would typically include summaries of feedback from legal professionals, potential users, or business development teams.)

### C. References

*   UK GDPR Article 28(3)
*   UK GDPR Article 32
*   ICO processor-contracts guidance
*   DPA 2018 overlays
*   Brainstorming Session Results: `docs/brainstorming-session-results.md`

## Next Steps

### Immediate Actions

1.  **Set up repo skeleton:** Create `analyzer/extract.py`, `engine.py`, `rules/processor_obligations.yaml`, and a basic FastAPI endpoint (`POST /review`). Install Windows dependencies (`pypdf`, `python-docx`, `fastapi`, `uvicorn`, `pytest`).
2.  **Write YAML stubs:** Draft initial `must_include`, `weak`, and `missing` signals for the 8 Art. 28(3) detectors.
3.  **Create gold set:** Collect 10-20 public/synthetic DPAs and label their outcomes for each detector.
4.  **Develop metrics script:** Create a script to run the gold set and output precision/recall, p95 latency.
5.  **Build basic UI:** Implement an issues table, coverage meter, and PDF export (HTML to PDF).

### PM Handoff

This Project Brief provides the full context for the GDPR Processor Obligations Checker. Please start in 'PRD Generation Mode', review the brief thoroughly to work with the user to create the PRD section by section as the template indicates, asking for any necessary clarification or suggesting improvements.
