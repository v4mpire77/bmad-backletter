# PR: Blackletter v0.0 MVP — Upload → Findings, Evidence Windows, HTML Reports

Branch: `feature/blackletter-v0-0-mvp`

## Summary

Implements the MVP pipeline end-to-end with deterministic behavior and Windows-first tooling.

## Key Changes

- Upload orchestration (jobs + statuses)
- Extraction (PDF/DOCX), sentences + page map
- Detector runner with weak-language downgrade and evidence windows (±2 by default)
- Rulepack pinning persisted on `Analysis`
- Job lifecycle timestamps (started/finished)
- Deterministic HTML report generation from stored artifacts
- Env wiring for split deploy (DATABASE_URL, NEXT_PUBLIC_API_BASE_URL)
- Deploy guide for Vercel (web) + Render (API) + Supabase (DB)

## Files of Interest

- `apps/api/blackletter_api/routers/contracts.py`
- `apps/api/blackletter_api/services/{extraction.py,detector_runner.py,evidence.py}`
- `apps/api/blackletter_api/routers/reports.py`, `services/reports.py`
- `apps/api/blackletter_api/database.py`
- `apps/web/src/lib/api.ts`
- `docs/deployment/vercel-render-supabase.md`

## How To Verify (Windows)

```
py -3.11 -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JOB_SYNC = "1"
uvicorn blackletter_api.main:app --app-dir apps/api --reload

# In another shell: upload and poll
python - << 'PY'
import io, httpx, fitz, time
base="http://127.0.0.1:8000"
d=fitz.open(); p=d.new_page(); p.insert_text((72,72),"We may process data. You should verify.")
buf=io.BytesIO(); d.save(buf); buf.seek(0)
r=httpx.post(f"{base}/api/contracts", files={"file": ("e2e.pdf", buf, "application/pdf")}); r.raise_for_status()
job=r.json().get("job_id") or r.json()["id"]; aid=r.json()["analysis_id"]
for _ in range(30):
  s=httpx.get(f"{base}/api/jobs/{job}").json()
  if s["status"] in ("done","error"): break; time.sleep(0.5)
print("status:", s["status"])
print("findings:", len(httpx.get(f"{base}/api/analyses/{aid}/findings").json()))
PY

# Generate report
python - << 'PY'
import httpx, json
base="http://127.0.0.1:8000"; aid=input("analysis_id: ")
resp=httpx.post(f"{base}/api/reports/{aid}", json={"include_logo": True, "include_meta": True, "date_format":"ISO"})
print(resp.status_code, json.dumps(resp.json(), indent=2))
PY
```

## Tests

- `python -m pytest -q apps/api/blackletter_api/tests/integration`
- `python -m pytest -q apps/api/blackletter_api/tests/unit/test_detector_runner.py`

## Notes / Follow-ups

- Report PDF export (Playwright/WeasyPrint) can build on the deterministic HTML
- Metrics wall (basic counters endpoint) to be added in a follow-up
- Minimal auth/settings to be introduced alongside Supabase

