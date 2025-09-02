import json
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.services.rulepack_loader import Rulepack, Detector, Lexicon
import blackletter_api.services.tasks as tasks


client = TestClient(app)


def test_job_lifecycle_sync(monkeypatch):
    # Force synchronous processing for deterministic test
    tasks.celery_app.conf.task_always_eager = True
    tasks.celery_app.conf.task_eager_propagates = True

    # Mock run_extraction to provide controlled extraction data
    mock_extraction_data = {
        "text_path": "extracted.txt",
        "page_map": [
            {"page": 1, "start": 0, "end": 100}
        ],
        "sentences": [
            {"page": 1, "start": 0, "end": 20, "text": "This document may contain sensitive information."},
            {"page": 1, "start": 21, "end": 45, "text": "You should review it carefully."},
            {"page": 1, "start": 46, "end": 70, "text": "It might be important."}
        ]
    }

    def mock_run_extraction(analysis_id: str, source_file: Path, out_dir: Path):
        # Create the mock extraction.json in the analysis directory
        extraction_path = out_dir / "extraction.json"
        with extraction_path.open("w", encoding="utf-8") as f:
            json.dump(mock_extraction_data, f)
        return extraction_path

    monkeypatch.setattr("blackletter_api.services.tasks.run_extraction", mock_run_extraction)

    # Mock the load_rulepack function
    mock_rulepack = Rulepack(
        name="test-rulepack",
        version="v1",
        detectors=[
            Detector(
                id="D001",
                type="lexicon",
                lexicon="weak-language",
                description="Detects weak language."
            )
        ],
        lexicons={
            "weak-language": Lexicon(
                name="weak-language",
                terms=["may", "might", "could", "should"]
            )
        }
    )
    monkeypatch.setattr("blackletter_api.services.detector_runner.load_rulepack", lambda: mock_rulepack)

    files = {
        "file": ("doc.pdf", BytesIO(b"dummy content"), "application/pdf"), # Content doesn't matter now
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
    analysis_dir = Path('.data') / 'analyses' / analysis_id
    
    extraction_path = analysis_dir / 'extraction.json'
    assert extraction_path.exists(), f"missing {extraction_path}"

    findings_path = analysis_dir / 'findings.json'
    assert findings_path.exists(), f"missing {findings_path}"

    # Verify findings content
    with findings_path.open("r") as f:
        findings = json.load(f)
    print(f"""
--- Findings Content ---
{json.dumps(findings, indent=2)}
""")
    
    # Verify extraction content
    with extraction_path.open("r") as f:
        extraction_data = json.load(f)
    print(f"""
--- Extraction Content ---
{json.dumps(extraction_data, indent=2)}
""")

    # Expect 3 findings for the 3 sentences with weak words
    assert len(findings) == 3
    for finding in findings:
        assert finding["verdict"] == "weak"
