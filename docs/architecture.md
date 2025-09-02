# System Architecture Overview

## Technology Stack
| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | Next.js 14, React, Tailwind, shadcn/ui | Server components, rapid dev, wide ecosystem |
| Backend | FastAPI (Python 3.11) | Async I/O, Pydantic v2, strong typing |
| Database | Postgres 15 + pgvector | ACID, row level security, vector search in same store |
| Cache & Queue | Redis + Celery | Shared cache, rate limits, background jobs |
| Storage | S3 or R2 | Durable object storage with lifecycle policies |
| LLM Providers | OpenAI/Gemini primary, Claude/Qwen fallback | Accuracy with failover |

## Project Structure
```
apps/
  web/        # Next.js frontend
  api/        # FastAPI service
rules/        # Rulepacks and lexicons
infra/        # Infrastructure as code
migrations/   # Database migrations
```

## Data Model Highlights
- **User**: id, email, role, org_id, mfa_enabled
- **Org**: id, name, plan, retention_days, data_residency
- **Document**: id, org_id, filename, checksum, storage_uri
- **AnalysisJob**: id, doc_id, status, duration_ms, failure_reason
- **Finding**: id, analysis_id, rule_id, verdict, severity, rationale, anchors[], evidence_window

## Key API Routes
- `POST /api/documents` – upload contract, returns job id
- `GET /api/documents/{id}/findings` – findings with anchors
- `GET /api/rulepacks` – list rulepacks and states
- `PUT /api/rulepacks/{id}` – enable/disable rulepack
- `GET /api/audit` – audit log export

## Non‑Functional Requirements
- p95 latency: auth ≤150 ms, findings ≤250 ms
- Analysis pipeline ≤60 s p95 for 40‑page PDF
- 100 orgs / 500 MAU initial scale, autoscaling workers
- GDPR by design: EU data residency, right to erasure, audit logging

## Environment & Secrets
- `DATABASE_URL`, `REDIS_URL`, `OPENAI_API_KEY`, `STRIPE_SECRET`, `NEXT_PUBLIC_API_URL`
- Secrets stored in platform vault, public env vars prefixed with `NEXT_PUBLIC_`
