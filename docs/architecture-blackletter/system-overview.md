# System Overview

Style: The architecture is a modern full-stack application consisting of a core API "monolith" (FastAPI), background workers (Celery with Redis), and a server-side rendered web application (Next.js).

## Principles

- Deterministic First: The core analysis engine relies on verifiable rulepacks, lexicons, and regex. LLM features are disabled by default.
- Evidence Everywhere: Every finding is traceable to a specific text snippet, ensuring auditability.
- Windows-Friendly DX: All development and setup scripts are designed to run seamlessly on Windows.
- Cost Minimal: The technology stack is chosen to leverage generous free tiers and low-cost managed services.

## High-level Services

- Web App: Next.js 14 (App Router) for uploads, dashboards, and the evidence viewer.
- API: FastAPI for ingestion, orchestration, and serving findings.
- Worker: Celery for long-running, asynchronous tasks like text extraction and rule analysis.
- Database & Cache: PostgreSQL 15 and Redis 7.x.
- Storage: S3-compatible object storage for documents and evidence.
