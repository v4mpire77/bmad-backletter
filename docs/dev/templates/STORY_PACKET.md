# STORY_PACKET.md — Story 1.1 Upload & Job Orchestration (Template)

- Story ID: 1.1
- Epic: 1 — Upload & Processing
- Status: Draft (planning output — no code changes)

## Summary
Implement upload endpoint and job orchestration for PDF/DOCX files up to 10MB, returning a queued job and creating an analysis record.

## Acceptance Criteria (from PRD/Templates)
- POST uploads accepts PDF/DOCX ≤10MB; returns `job_id`
- GET jobs/{id} returns status: queued|running|done|error (+ error reason)
- On done, analysis record exists with filename, size, created_at
- Latency budget: enqueue < 500ms server time

## Out of Scope
- OCR path (off by default)
- Detector execution and reports (future stories)

## Architecture Notes
- API service: FastAPI routers/services
- Storage: abstracted via service layer (mock or local fs in MVP)
- Determinism: pin rulepack versions when introduced

## Allowed Repo Surface (story 1.1)
- apps/api/blackletter_api/routers/uploads.py
- apps/api/blackletter_api/services/tasks.py
- apps/api/blackletter_api/models/entities.py
- apps/web/src/app/new/page.tsx
- tests/unit/api/test_uploads.py
- tests/integration/test_upload_flow.py

## Data Contracts (MVP)
- POST /uploads: multipart form; returns `{ job_id, analysis_id, status: 'queued' }`
- GET /jobs/{id}: `{ id, status, error? }`

## Risks & Mitigations
- Large files: enforce size limit at router and server config
- Content type spoofing: validate MIME + extension + magic header
- Async queue: use in‑proc stub for MVP; swap to real broker later

## Open Questions
- Storage backend in MVP? (local vs cloud)
- Virus scanning integration timing?

## Links
- PRD: docs/prd/8-detailed-story-templates-for-sm-dev.md
- Stories root: docs/stories/

