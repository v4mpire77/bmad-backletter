# Render Deployment — Docker All-in-One

This guide deploys the monorepo as a single Docker Web Service on Render, serving both the Next.js web app and the FastAPI API behind Nginx.

## One-Click via render.yaml

The repository includes `render.yaml` at the root:

```yaml
services:
  - type: web
    name: blackletter-all-in-one
    env: docker
    autoDeploy: true
    healthCheckPath: /
```

In Render, click New → Blueprint and select the repository. Confirm the service configuration and deploy.

## Manual Setup via Dashboard

1. New → Web Service → Connect repository.
2. Environment: Docker.
3. Health Check Path: `/` (or `/healthz`).
4. No build/start commands needed (Dockerfile handles it).
5. Deploy.

## Verify

- Visit the service URL: `/` should show the landing page (SSR).
- API endpoints:
  - `GET /api` → `{ "status": "ok" }`
  - `GET /healthz` → `{ "ok": true }`
- Logs: should show Nginx, Next.js started on `:3000`, and Uvicorn on `:8000`.

## Configuration

- Nginx listens on `$PORT` provided by Render. Do not override `PORT` in env vars.
- Internal ports: Next.js on `3000`, FastAPI on `8000`.
- Same-origin architecture: no CORS configuration required.

## Rollback

- In Render, open the service → Deploys → select a previous successful deploy → Rollback.

## Regions and Performance

- Choose the region closest to your users. If you later split web/API providers, try to keep regions aligned to reduce latency.

