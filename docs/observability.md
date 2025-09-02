# Observability

This project emits structured logs to aid debugging of asynchronous jobs.

HTTP requests are logged via a middleware that records method, path,
status code, and duration. Uvicorn's access log is disabled to keep output
consistent.

## Log Fields

Each job state transition includes the following fields:

- `job_id`
- `tenant_id`
- `state`
- `attempt`
- `queued_at`
- `started_at`
- `finished_at`
- `duration_ms`
- `error_type`
- `error_msg`

## Sample Log Lines

```json
{"level": "INFO", "message": "task_start", "job_id": "123", "state": "start"}
{"level": "INFO", "message": "task_success", "job_id": "123", "state": "success", "duration_ms": 345}
{"level": "INFO", "message": "job_status_request", "job_id": "123", "path": "/api/jobs/123"}
```

## Tailing Logs

Run the API or worker with JSON logging enabled:

```bash
LOG_FORMAT=json uvicorn apps.api.blackletter_api.main:app --reload --log-config=None
LOG_FORMAT=json celery -A apps.api.blackletter_api.worker_app worker -l info
```

Filter for a specific job:

```bash
# Using jq
uvicorn ... | jq 'select(.job_id=="123")'
```
