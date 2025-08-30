# Split Deploy: Vercel (Web) + Render (API) + Supabase (DB)

This guide deploys the Next.js frontend to Vercel and the FastAPI backend to Render, with optional Supabase Postgres.

## Overview

- Web (Vercel): `apps/web`
- API (Render): `apps/api/blackletter_api`
- DB (Supabase, optional for MVP): replace SQLite via `DATABASE_URL`

## Prerequisites

- GitHub repo connected to both Vercel and Render
- Working main branch (or feature branch) with passing API health (`/healthz`)

## API on Render

1) Create a Web Service from the repo
- Root: repo root
- Start command: `uvicorn blackletter_api.main:app --host 0.0.0.0 --port $PORT --app-dir apps/api`

2) Add a persistent disk (recommended)
- Mount path: `/var/data`
- Set env: `DATA_ROOT=/var/data`

3) Environment Variables
- `APP_ENV=prod`
- `DATA_ROOT=/var/data`
- `CORS_ORIGINS=https://<your-vercel-domain>`
- `EVIDENCE_WINDOW_BEFORE=2`
- `EVIDENCE_WINDOW_AFTER=2`
- Optional (token policy): `TOKEN_CAP_ENABLED=0`
- Optional (DB): `DATABASE_URL=postgresql+psycopg://<user>:<pass>@<host>:5432/<db>`

4) Health Check
- Path: `/healthz`

## Web on Vercel

1) Import the GitHub repo
- Project: `apps/web` (Next.js 14)

2) Environment Variables
- `NEXT_PUBLIC_API_BASE_URL=https://<render-service-domain>`

3) Build
- Framework: Next.js (auto)

## Supabase (Optional, Phase 2)

1) Create a Supabase project (Postgres)
- Note the connection string (user/pass/host/db)

2) Set on Render service
- `DATABASE_URL=postgresql+psycopg://<user>:<pass>@<host>:5432/<db>`

3) Migrations (later)
- For MVP, the API can auto-create tables; for production, add alembic migrations.

## Local Verification

    # API
    $env:JOB_SYNC="1"
    uvicorn blackletter_api.main:app --app-dir apps/api --reload
    # Web
    cd apps/web; npm run dev

## Notes

- For all-in-one Render Docker deploy, see `docs/deployment/render.md`.
- SQLite remains default locally. Switching to Postgres requires only `DATABASE_URL`.

