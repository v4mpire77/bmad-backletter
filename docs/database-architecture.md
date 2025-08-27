# Database Architecture

## Summary

Outlines storage strategy for application data and metadata.

## Engine & Topology

- **SQLite** for local development and automated tests.
- **PostgreSQL** in Phase‑2 for multi‑user deployments.

## Schema Highlights

- `jobs` – track processing state for uploaded contracts.
- `analyses` – coverage stats and verdict summaries.
- `findings` – individual detector results with offsets.

## Migrations

- Managed with Alembic.
- Linear migration history checked into VCS.

## Indexing & Performance

- Index `jobs.status` and `findings.analysis_id` for fast lookups.
- Use `GIN` indexes for JSONB fields once on Postgres.

## Backup & Recovery

- Dev: copy SQLite file as artefact.
- Prod: daily logical dumps + point‑in‑time recovery.
