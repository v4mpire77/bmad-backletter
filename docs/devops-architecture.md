# DevOps / Infrastructure Architecture

## Summary

Describes how Blackletter services are built, deployed and observed.

## Environments

- **dev** – local containers and SQLite.
- **staging** – mirrors prod; used for QA.
- **prod** – managed deployment with Postgres and object storage.

## CI/CD Pipeline

1. Lint & test on push.
2. Build backend container image.
3. Publish artefacts to registry.
4. Deploy to staging on merge to `main`.
5. Manual promotion to prod with approval.

## Infrastructure Components

- Container runtime: Docker.
- Orchestration: minimal `docker compose` in MVP; evaluate Kubernetes later.
- Secrets managed via environment variables and platform store.

## Observability

- Structured logs with request IDs.
- Metrics: latency, token usage, explainability percentage.
- Health probes: `/healthz`, `/readyz`.
