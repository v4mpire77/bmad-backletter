# Epic E1: Ingestion & Extraction

## Story E1.1: Upload & Job Orchestration

- POST `/contracts` accepts PDF/DOCX up to 10MB; returns `job_id` and job status endpoint.

## Story E1.2: Text Extraction

- Extract text, page map, and sentence index; store artifacts and link to analysis records.

## Story E1.3: Evidence Window Builder

- Build ±2 sentence evidence windows and handle page boundaries.
