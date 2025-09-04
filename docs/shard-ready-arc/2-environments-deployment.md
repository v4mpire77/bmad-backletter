# Environments & Deployment

Environments: local (Windows), staging, prod.

## Local (Windows)

- Docker Desktop + Compose: A docker-compose.local.yml will manage containers for the api, web app, worker, db (Postgres), and redis.
- PowerShell Scripts: A suite of scripts in tools/windows/ will handle bootstrapping, running, testing, and linting the entire application.

## Production (Recommended)

- Web (Next.js): Vercel, for its seamless integration with Next.js and global CDN.
- API / Worker: Render, using a Web Service for the API and a Background Worker for Celery.
- Database: A managed Postgres service like Neon, Supabase, or Render's offering.
- Redis: Upstash for its serverless, low-cost Redis instances.
- Storage: An S3-compatible service like Cloudflare R2 or Supabase Storage.
- CI/CD: GitHub Actions will be used to run tests on every pull request and deploy to staging/production environments upon merge to the respective branches.
