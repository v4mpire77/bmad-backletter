# Story 3.1 — Docker All‑in‑One (Dev Guide)
Status: Approved

Package Next.js and FastAPI behind Nginx for local and Render deployment.

## Summary
Single image that runs Nginx on `$PORT`, proxies `/api/*` to FastAPI `:8000` and other routes to Next.js `:3000`.

## Allowed Repo Surface
- deploy/docker/Dockerfile
- deploy/docker/nginx.conf.template
- deploy/docker/start.sh
- render.yaml
- docs/deployment/{docker-local.md,render.md}

## Implementation Steps
- Multi-stage: build web, install API deps, copy into runtime image with Nginx and Supervisor or start script.
- Nginx config with gzip, cache for static assets, proxy headers, timeouts.
- start.sh: launch uvicorn and next start; wait-for scripts if needed.

## Tests
- Build/run locally; verify `/` and `/api/healthz` work; CORS not required due to same origin.

