# 6) API Contracts (MVP — frozen)

* `POST /api/contracts` → `{ job_id, analysis_id, status:'queued' }`
* `GET /api/jobs/{job_id}` → job status
* `GET /api/analyses/{id}` → summary + coverage
* `GET /api/analyses/{id}/findings` → `Finding[]`
* `POST /api/reports/{analysis_id}` → `{ url }`

Full JSON shapes live in `docs/architecture/api_contracts.md`.
