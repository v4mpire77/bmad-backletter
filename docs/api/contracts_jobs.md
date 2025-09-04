
# Contracts & Jobs API

This document summarizes the upload and job status endpoints.

- Base prefix: `/api`

POST `/api/contracts`
- Purpose: Upload a contract (PDF or DOCX, ≤10MB) and enqueue background processing.
- Request: multipart/form-data with field `file`.
- Validations:
  - Content types: `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
  - Max size: 10MB (413 on exceed).
- Responses:
  - 201: `{ id, job_id, status, analysis_id }` where `status` starts as `queued`.
  - 415: `{ code: "unsupported_file_type", message: string }`.
  - 413: `{ code: "file_too_large", message: string }`.
- Storage: Deterministic path `.data/analyses/{analysis_id}/<sanitized-name>.<ext>`.
- Privacy: Filenames/content not logged.

GET `/api/jobs/{id}`
- Purpose: Poll job status.
- Response:
  - 200: `{ id, job_id, status: queued|running|done|error, analysis_id, error }`.
  - 404: `{ code: "not_found", message: "Job not found" }`.

Background Processing
- A Celery task `process_job` runs extraction and detection.
- Job state is persisted in Redis: `queued → running → done|error`.
- Artifacts: `.data/analyses/{analysis_id}/extraction.json`, derived evidence, and HTML export.
