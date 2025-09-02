# API Architecture

## Summary

Describes RESTful contract for Blackletter services and how clients interact with them.

## Design Principles

- **Explicit contracts** via OpenAPI.
- **Deterministic responses**; no hidden fields.
- **Versioned** endpoints under `/api` with semantic versioning.

## Core Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/contracts` | Ingest a new contract file and create job + analysis IDs. |
| `GET` | `/api/jobs/{id}` | Poll job status until processing completes. |
| `GET` | `/api/analyses/{id}` | Retrieve analysis summary and coverage metrics. |
| `GET` | `/api/analyses/{id}/findings` | Fetch detector findings for a given analysis. |
| `POST` | `/api/reports/{analysis_id}` | Trigger PDF export and return download URL. |

## Authentication

- Phase‑1: none; local development only.
- Phase‑2: bearer tokens with minimal Admin/Reviewer roles.

## Error Handling

- Errors return `{ "code": <error_code>, "detail": <message> }`.
- `code` is one of the enums in `apps/api/blackletter_api/services/errors.py`.
- 4xx for client issues, 5xx for server faults.

## Rate Limits

- MVP: none.
- Future: per‑org quotas enforced at gateway.

## Documentation

OpenAPI spec is generated from FastAPI app and published at `/openapi.json`.
