# System Overview

Style: The architecture is a modern full-stack application consisting of a core API "monolith" (FastAPI), background workers (Celery with Redis), and a server-side rendered web application (Next.js).

## Principles

- Deterministic First: The core analysis engine relies on verifiable rulepacks, lexicons, and regex. LLM features are disabled by default.
- Evidence Everywhere: Every finding is traceable to a specific text snippet, ensuring auditability.
- Windows-Friendly DX: All development and setup scripts are designed to run seamlessly on Windows.
- Cost Minimal: The technology stack is chosen to leverage generous free tiers and low-cost managed services.

## High‑level Services

- Web App: A Next.js 14 (App Router) application for all user interactions, including uploads, dashboards, and the evidence viewer.
- API: A FastAPI service that handles contract ingestion, job orchestration, and serves findings to the frontend.
- Worker: A Celery-based worker process for handling long-running, asynchronous tasks like text extraction and rule-based analysis.
- Database & Cache: PostgreSQL for persistent storage and Redis as a message broker for Celery and for caching.
- Storage: An S3-compatible object storage for uploaded documents and generated reports.
