# Upload Page States and Polling

The `/upload` page accepts PDF or DOCX files up to 10MB. Client-side validation
shows inline messages for invalid type or size.

After a file is posted to `/api/contracts`, the API responds with a `job_id` and
a `202 Accepted` status. The front end polls `GET /api/jobs/{id}` every two
seconds. After three consecutive failures the interval backs off exponentially
(4s, 8s, ...).

Job status values are mapped to four UI states:

- **queued** – waiting for a worker
- **processing** – worker running; progress bar shows `progress` if provided
- **done** – analysis finished; link to view results
- **failed** – error during processing; user may retry the upload

If the API includes `eta` or `progress`, the progress bar is determinate;
otherwise it falls back to an indeterminate animation.
