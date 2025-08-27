# Docker Local Run — All-in-One

Build and run the combined Next.js + FastAPI + Nginx container locally.

## Prerequisites

- Docker Desktop or Docker Engine

## Build

```bash
docker build -f deploy/docker/Dockerfile -t blackletter-all-in-one .
```

## Run

```bash
docker run --rm -p 8080:8080 blackletter-all-in-one
# Open http://localhost:8080
# API health: http://localhost:8080/api and /healthz
```

## Notes

- The container runs three processes: Uvicorn (FastAPI), Next.js (SSR), and Nginx.
- Nginx listens on `$PORT` (defaults to 8080 locally) and proxies:
  - `/api/*` → Uvicorn on `:8000`
  - `/*` → Next.js on `:3000`
- Logs are written to stdout/stderr for visibility.

