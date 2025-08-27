# Story 1.1 — Upload & Job Orchestration (Dev Guide)
Status: Approved

Authoritative dev instructions for implementing Story 1.1 with zero ambiguity.

## Story Summary
Accept PDF/DOCX uploads (≤10MB), enqueue analysis job, return `{ job_id, analysis_id, status:'queued' }`. Jobs endpoint returns status; on done, an analysis record exists.

## Allowed Repo Surface
- `apps/api/blackletter_api/routers/uploads.py`
- `apps/api/blackletter_api/services/tasks.py`
- `apps/api/blackletter_api/models/entities.py`
- `apps/web/src/app/new/page.tsx`
- `tests/unit/api/test_uploads.py`
- `tests/integration/test_upload_flow.py`

## Implementation Steps
- API Router `uploads.py` (FastAPI)
  - POST `/api/uploads` (multipart)
  - Validate: content-type PDF/DOCX; size ≤10MB (fail with 400)
  - Create analysis id (UUID); call `services.tasks.enqueue('analyze', { analysis_id })`
  - Return 200 `{ job_id, analysis_id, status:'queued' }`
  - TODO: virus scan, signed URLs, storage provider
- Services `tasks.py`
  - Add `enqueue(kind: str, payload: dict) -> str` returns `job_id`
  - MVP: in-memory queue stub + status map
  - TODO: swap to real broker
- Models `entities.py`
  - Define minimal `Analysis` record (id, filename, size, created_at)
  - TODO: persistence (future story)
- Web `/new`
  - On success, optionally display “Queued” → “Done” (mock already exists); keep interface compatible

## Data Contracts
- POST `/api/uploads`
  - Request: multipart file `file`
  - Response 200: `{ job_id: string, analysis_id: string, status: 'queued' }`
  - Errors: 400 invalid type/size
- GET `/api/jobs/{id}` (existing or stub to be added in jobs story)

## Tests
- Unit: `tests/unit/api/test_uploads.py`
  - Accepts valid PDF/DOCX; rejects others
  - Enforces ≤10MB
  - Calls `tasks.enqueue('analyze', {analysis_id})`
- Integration: `tests/integration/test_upload_flow.py`
  - POST upload → queued payload, job id present
  - Poll (stub) job status → done (simulated)

## Windows Commands
- API run: `cd apps/api; uvicorn blackletter_api.main:app --reload`
- Unit tests: `pytest apps/api/blackletter_api/tests/unit -q`
- Integration: `pytest apps/api/blackletter_api/tests/integration -q`

## Do / Don’t
- Do: keep router thin; validate inputs; defer business logic to services
- Don’t: store files or implement extraction here; add TODOs instead
- Do: pin limits and content-types in one place (constants)
