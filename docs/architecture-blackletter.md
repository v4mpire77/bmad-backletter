# Blackletter — Fullstack Architecture (shard)

This shard contains the system overview, environments & deployment, and the technology stack for the Blackletter project.

## System Overview

Style: The architecture is a modern full-stack application consisting of a core API "monolith" (FastAPI), background workers (Celery with Redis), and a server-side rendered web application (Next.js).

### Principles

- Deterministic First: The core analysis engine relies on verifiable rulepacks, lexicons, and regex. LLM features are disabled by default.
- Evidence Everywhere: Every finding is traceable to a specific text snippet, ensuring auditability.
- Windows-Friendly DX: All development and setup scripts are designed to run seamlessly on Windows.
- Cost Minimal: The technology stack is chosen to leverage generous free tiers and low-cost managed services.

### High-level Services

- Web App: Next.js 14 (App Router) for uploads, dashboards, and the evidence viewer.
- API: FastAPI for ingestion, orchestration, and serving findings.
- Worker: Celery for long-running, asynchronous tasks like text extraction and rule analysis.
- Database & Cache: PostgreSQL 15 and Redis 7.x.
- Storage: S3-compatible object storage for documents and evidence.

## Environments & Deployment

Environments: local (Windows), staging, production.

Local (Windows):

- Docker Desktop + Compose: `docker-compose.local.yml` manages api, web, worker, db, and redis.
- PowerShell runbooks in `tools/windows/` provide `dev.ps1`, `test.ps1`, and `migrate.ps1`.

Production (recommended):

- Web: Vercel for Next.js hosting and CDN.
- API/Worker: Render (Web Service + Background Worker for Celery).
- DB: Managed Postgres (Neon/Supabase/Render).
- Redis: Upstash (serverless Redis).
- Storage: Cloudflare R2 or Supabase Storage.
- CI/CD: GitHub Actions (lint, test, smoke, deploy).

## Technology Stack (pinned)

| Category | Technology | Version |
|---|---|---|
| Frontend Language | TypeScript | 5.4.x |
| Frontend Framework | Next.js | 14.2.x |
| UI Library | React | 18.2.x |
| UI Components | shadcn/ui | latest |
| Styling | Tailwind CSS | 3.4.x |
| Backend Language | Python | 3.11 |
| Backend Framework | FastAPI | 0.111.x |
| ORM | SQLAlchemy | 2.0.x |
| Migrations | Alembic | latest |
| Async Tasks | Celery | 5.3.x |
| Database | PostgreSQL | 15 |
| Cache / Broker | Redis | 7.x |
| Storage | S3-compatible | - |
| Testing FE | Vitest / RTL | latest |
| E2E | Playwright | latest |
| Testing BE | Pytest | latest |
| CI/CD | GitHub Actions | - |

Notes: pin versions in CI and the repo manifests to ensure reproducible builds and deterministic behavior.
