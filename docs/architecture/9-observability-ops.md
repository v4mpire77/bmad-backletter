# 9) Observability & Ops

* **Logging**: structured, request IDs, no raw snippet bodies.
* **Metrics**: p50/p95 latency, tokens/doc, %LLM usage, explainability %.
* **Health**: `/healthz`, `/readyz`.
* **Config**: `core-config.yaml` logged on boot (effective values).
* **Backups**: SQLite file in dev; Postgres with backups in Phase 2.
  Details in `docs/operational_architecture.md`.
