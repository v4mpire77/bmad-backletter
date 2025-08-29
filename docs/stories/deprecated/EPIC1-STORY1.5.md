# Story 1.5: Logging & Basic Metrics

**ID:** EPIC1-STORY1.5

**As an admin, I want structured logs and latency metrics so I can trace job flow and detect errors early.**

## Tasks:
* Implement structured JSON logging for key job events.
* Capture and log latency metrics at key stages (e.g., enqueue_time, extraction_time).

## Acceptance Criteria:
* All logs are in a structured JSON format with `job_id` and `analysis_id` as correlation IDs.
* Latency metrics are logged with a timestamp and a clear description.
* A simple admin dashboard or log viewer shows a live stream of these logs.

## Test Fixtures:
* **Validation:** Verify that a test run produces a stream of structured logs in the console.

## Artifacts:
* `log_format_spec.json` (example log entry).

---

## Dev Agent Record

- Status: **COMPLETE** ✅
- Agent Model Used: dev (James)

### Tasks / Subtasks Checkboxes
- [x] Implement structured JSON logging for key job events
- [x] Capture and log latency metrics at key stages (enqueue_time, extraction_time)
- [x] Create admin dashboard for log viewing with real-time streaming
- [x] Implement correlation ID tracking (`job_id`, `analysis_id`) throughout pipeline
- [x] Add comprehensive logging to all major API endpoints
- [x] Create log format specification document

### Debug Log References
- Structured logging configured in `main.py` with custom JSON formatter
- Latency metrics captured in `services/tasks.py` for extraction and detection
- Upload latency tracking added to `routers/contracts.py`
- Request latency tracking added to `routers/jobs.py`
- Admin dashboard available at `docs/artifacts/admin_dashboard.html`

### Completion Notes
- **Structured JSON logging** implemented with correlation IDs (`job_id`, `analysis_id`)
- **Latency metrics** captured at key stages: upload, extraction, detection, API requests
- **Admin dashboard** provides real-time log streaming with metrics aggregation
- **Log format specification** documents the complete logging structure
- All major endpoints now include comprehensive logging with performance tracking

### File List
- Modified: `apps/api/blackletter_api/main.py` - Added structured JSON logging setup
- Modified: `apps/api/blackletter_api/routers/contracts.py` - Added upload logging and latency tracking
- Modified: `apps/api/blackletter_api/routers/jobs.py` - Added job status logging and request latency
- Added: `docs/artifacts/admin_dashboard.html` - Admin dashboard for log viewing
- Added: `docs/artifacts/log_format_spec.json` - Log format specification

### Change Log
- feat(logging): implement structured JSON logging with correlation IDs
- feat(metrics): add latency tracking for upload, extraction, and detection operations
- feat(admin): create real-time admin dashboard for logs and metrics
- docs(spec): add comprehensive log format specification
