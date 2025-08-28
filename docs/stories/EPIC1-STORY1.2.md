# Story 1.2: Job Status Tracking

**ID:** EPIC1-STORY1.2

**As a user, I want to see the progress of my uploaded document so I know if it is queued, running, or finished.**

## Tasks:
* Implement the `GET /api/jobs/{id}` endpoint to return the job status.
* Build a front-end UI component that polls the status endpoint.
* Create a visual stepper component to show the job progress (e.g., Queued → Extracting → Detecting → Done).

## Acceptance Criteria:
* The endpoint must return `{ "job_id": "uuid", "status": "string", "error": "string" }` (if applicable).
* The UI must update in near real-time as the job status changes without a full page refresh.

## Test Fixtures:
* **Success Case:** Poll a job that is successfully completed.
* **Failure Case:** Poll a job that results in an error state.

## Artifacts:
* `GET /api/jobs/{id}` API contract.
* Job status UI component mock.

---

## Dev Agent Record

- Status: Ready for Review
- Agent Model Used: dev (James)

### Tasks / Subtasks Checkboxes
- [x] Implement the `GET /api/jobs/{id}` endpoint to return the job status.
- [x] Build a front-end UI component that polls the status endpoint (`docs/artifacts/job_status_ui.html`).
- [x] Create a visual stepper component in the demo uploader (`docs/artifacts/job_status_demo.html`).
- [x] Alias `error_reason` to serialize as `error` in API responses.

### Debug Log References
- `.venv\\Scripts\\python.exe -m pytest apps/api/blackletter_api/tests/integration/test_job_polling_status.py -q`
- `.venv\\Scripts\\python.exe -m pytest apps/api/blackletter_api/tests -q`

### Completion Notes
- `GET /api/jobs/{id}` returns `id`, `job_id`, `status`, `analysis_id`, and `error` (alias of `error_reason`).
- Added polling tests for async success and error paths.
- Added minimal polling UI and uploader demo with stepper to visualize progress.

### File List
- Modified: `apps/api/blackletter_api/models/schemas.py`
- Modified: `apps/api/blackletter_api/routers/jobs.py`
- Added: `apps/api/blackletter_api/tests/integration/test_job_polling_status.py`
- Added: `docs/artifacts/job_status_ui.html`
- Added: `docs/artifacts/job_status_demo.html`

### Change Log
- feat(api): expose `error` alias and include `job_id` in job status
- test(api): add integration tests for job polling (success and error)
- docs(ui): add minimal polling UI and stepper demo
