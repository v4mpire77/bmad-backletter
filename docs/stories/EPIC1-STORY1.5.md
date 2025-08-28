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
