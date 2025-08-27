# Story 3.2 — Report Export (Dev Guide)
Status: Approved

Render explainable HTML and generate PDF via Playwright; persist under reports/.

## Summary
Build a deterministic HTML report from stored artifacts; convert to PDF when requested; list reports via API.

## Allowed Repo Surface
- apps/api/blackletter_api/services/report_renderer.py
- apps/api/blackletter_api/routers/reports.py
- apps/web/src/components/ExportDialog.tsx (wire to API)
- apps/web/src/app/reports/page.tsx
- apps/api/blackletter_api/tests/unit/test_report_renderer.py
- apps/api/blackletter_api/tests/integration/test_report_flow.py

## Implementation Steps
- HTML renderer (Jinja2) with headings, verdicts, snippets, timestamps and metadata; CSS inline.
- Playwright to PDF (server-side) with stable viewport; write `.data/analyses/{id}/reports/{report_id}.pdf` (and .html).
- API: POST `/api/reports/{analysis_id}` body `{ format, include_logo?, include_metadata?, date_format? }` → `{ report_id, url }`; GET list.

## Tests
- Golden HTML snapshot; PDF magic header and byte size sanity; error handling for missing artifacts.

