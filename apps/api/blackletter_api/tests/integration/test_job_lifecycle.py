from __future__ import annotations

import os
import json
from io import BytesIO
from time import sleep

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_job_lifecycle_sync(monkeypatch):
    # Force synchronous processing for deterministic test
    monkeypatch.setenv("JOB_SYNC", "1")

    files = {
        "file": ("doc.pdf", BytesIO(b"%PDF-1.4 minimal"), "application/pdf"),
    }
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    job_id = data["id"]
    analysis_id = data["analysis_id"]
    assert data["status"] == "queued"

    # Immediately check job status
    s = client.get(f"/api/jobs/{job_id}")
    assert s.status_code == 200
    sd = s.json()
    assert sd["id"] == job_id
    assert sd["analysis_id"] == analysis_id
    # Since sync, status should be done
    assert sd["status"] in ("running", "done")
    
    # Verify artifacts exist
    from pathlib import Path
    analysis_dir = Path('.data') / 'analyses' / analysis_id
    
    extraction_path = analysis_dir / 'extraction.json'
    assert extraction_path.exists(), f"missing {extraction_path}"

    findings_path = analysis_dir / 'findings.json'
    assert findings_path.exists(), f"missing {findings_path}"

    # Verify findings content
    with findings_path.open("r") as f:
        findings = json.load(f)
    assert len(findings) == 1
    assert findings[0]["verdict"] == "pass"
