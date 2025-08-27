# TEST_PLAN.md — Story 1.1 Upload & Job Orchestration (Template)

## Scope
Validate upload endpoint, size/type checks, job enqueue, and status polling for Story 1.1.

## Environments
- Local dev (Windows PowerShell): Node 18+, Python 3.11+, uvicorn
- Env vars via `.env` (no real secrets)

## Unit Tests (API)
- tests/unit/api/test_uploads.py
  - Accepts PDF/DOCX ≤10MB, rejects others
  - Returns `{ job_id, analysis_id, status:'queued' }`
  - Calls `services.tasks.enqueue('analyze', {analysis_id})`

## Integration Tests
- tests/integration/test_upload_flow.py
  - POST /uploads → 202/200 with queued payload
  - GET /jobs/{id} transitions queued → running → done (stubbed)
  - On done, analysis record present (stubbed)

## Non‑Functional
- Enqueue latency < 500ms server time (measure mocked path)
- Deterministic responses under mocks

## Test Data
- Synthetic small PDF/DOCX fixtures: 1–2KB
- Malformed/oversized files for negative tests

## Commands
- API: `cd apps/api && uvicorn blackletter_api.main:app --reload`
- Unit: `pytest apps/api/blackletter_api/tests/unit -q`
- Integration: `pytest apps/api/blackletter_api/tests/integration -q`
- Windows helpers: `scripts\ps*.ps1` (optional wrappers)

## Acceptance
- All AC scenarios green; coverage ≥80% on changed code
- Lint clean; no secrets in logs

