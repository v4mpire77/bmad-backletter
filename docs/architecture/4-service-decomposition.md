# 4) Service Decomposition

* **routers/**

  * `uploads.py` (POST /api/contracts)
  * `jobs.py` (GET /api/jobs/{id})
  * `analyses.py` (GET /api/analyses/{id}[ /findings])
  * `reports.py` (POST /api/reports/{analysis_id})
* **services/**

  * `extraction.py` (PDF/DOCX → text + page map)
  - `evidence.py` (evidence window builder ±N sentences)
  * `detection.py` (load rules; run detectors a–h; produce Finding[])
  * `reporting.py` (render HTML→PDF; export URL)
  * `metrics.py` (p95 latency, tokens/doc, explainability %)
  * `llm_gate.py` (provider off by default; snippet-only with PII redaction)
  * `tasks.py` (FastAPI BackgroundTasks MVP; Phase 2 Celery)
* **models/**

  * `schemas.py` (Pydantic models: Finding, Analysis, Job)
  * `entities.py` (ORM entities)
  * `db.py` (SQLite dev; Phase 2 Postgres)
* **rules/**

  * `art28_v1.yaml` (detectors a–h)
  * `lexicons/weak_language.yaml`
* **config**

  * `core-config.yaml` (authoritative runtime toggles)

The canonical **source tree** is tracked in `docs/architecture/source_tree.md`.
