# Project Brief: GDPR Processor Obligations Checker (v2)

## Executive Summary

This project, "Blackletter," will create a rules-first, cost-efficient system to automatically check GDPR processor agreements for compliance with Article 28(3). It is designed to solve the problem of slow, inconsistent, and time-consuming manual contract reviews for legal professionals by offering a transparent, auditable, and highly accurate solution that minimizes reliance on expensive LLM calls.

## Problem Statement

Legal professionals currently spend 2-6 hours manually reviewing each contract to ensure GDPR Article 28(3) compliance. This process is prone to inconsistency, fatigue, and human error, leading to potential missed clauses. Existing "AI compliance" tools often lack transparency, are expensive, and provide "black-box" results without clear evidence, leading to a lack of trust and auditability.

## Proposed Solution

The proposed solution is a rules-first GDPR processor-obligations checker. It will ingest PDF and DOCX contracts, extract the relevant clauses, and apply a curated YAML/regex rule engine to identify compliance issues. LLMs will be used sparingly, only for highly ambiguous or borderline cases, to keep costs near-zero. The system will output a structured report with detailed findings, a coverage map, and an auditable trail of evidence, including clause snippets and citations.

## Target Users

*   **Primary User Segment:** Small to Medium Law Firms & Solo Practitioners who need to ensure compliance efficiently and affordably.
*   **Secondary User Segment:** In-house Legal Teams at SMEs who need to streamline internal compliance processes and reduce legal risk.

## Goals & Success Metrics

### Business Objectives
*   Achieve a p95 latency of ≤ 60 seconds per document.
*   Maintain an average cost per document of ≤ £0.10.
*   Attain precision ≥ 0.85 and recall ≥ 0.90 on the gold set.

### User Success Metrics
*   Reduce manual contract review time by at least 60%.
*   Achieve "zero missed compliance flags" for GDPR Art. 28(3) obligations.
*   Maintain an explainability rate of ≥ 95%.

## MVP Scope

### Core Features
*   PDF/DOCX Ingestion & Text Extraction.
*   8 GDPR Art. 28(3) Detectors using a rules-first engine.
*   Snippet-only LLM integration with a hard token cap.
*   Evidence-first UI with a coverage meter.
*   PDF/HTML export of compliance reports.
*   Token & latency logger.
*   Gold set evaluation for precision/recall.
*   Local SQLite cache.

### Out of Scope for MVP
*   Full LLM-based clause generation or redlining.
*   Batch processing of documents.
*   Cloud persistence of uploaded documents.
*   Advanced analytics dashboards.

## Post-MVP Vision

*   **Phase 2:** Expand the weak-language lexicon, implement a local classifier to reduce LLM calls, and build a "metrics wall" in the UI.
*   **Long-term:** Evolve into an "Autonomous Compliance Counsel" with capabilities for drafting opinions, real-time risk monitoring, and a legal-grade RAG system.

## Technical Considerations

*   **Platform:** Windows-first for the MVP.
*   **Technology Stack:** Python (FastAPI) for the backend, Next.js for the frontend, and SQLite for the MVP database.
*   **Architecture:** A modular, single-process HTTP application with a clear separation of concerns.

## Constraints & Assumptions

*   **Constraints:** A hard budget cap of ≤ £0.10 per document, a rapid MVP timeline, and a lean development team.
*   **Assumptions:** Deterministic rules can cover the majority of compliance checks, and users value transparency and auditability over "black-box" AI.

## Risks & Open Questions

*   **Risks:** Clause variance in contracts, potential for LLM "hallucination," and the risk of users over-relying on the tool for legal advice.
*   **Open Questions:** What are the precise acceptance wordings for each Art. 28(3) duty, and what is the optimal strategy for expanding the weak-language lexicon?

