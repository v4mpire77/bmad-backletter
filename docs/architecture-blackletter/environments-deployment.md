# Environments & Deployment

Environments: local (Windows), staging, production.

## Local (Windows)

- Docker Desktop + Compose: `docker-compose.local.yml` manages api, web, worker, db, and redis.
- PowerShell runbooks in `tools/windows/` provide `dev.ps1`, `test.ps1`, and `migrate.ps1`.

## Production (recommended)

- Web: Vercel for Next.js hosting and CDN.
- API/Worker: Render (Web Service + Background Worker for Celery).
- DB: Managed Postgres (Neon/Supabase/Render).
- Redis: Upstash (serverless Redis).
- Storage: Cloudflare R2 or Supabase Storage.
- CI/CD: GitHub Actions (lint, test, smoke, deploy).
