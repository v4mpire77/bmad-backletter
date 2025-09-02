from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.services.rulepack_loader import Rulepack, Detector, Lexicon


client = TestClient(app)


def test_get_findings_by_job(monkeypatch) -> None:
    monkeypatch.setenv("JOB_SYNC", "1")

    mock_extraction_data = {
        "text_path": "extracted.txt",
        "page_map": [{"page": 1, "start": 0, "end": 100}],
        "sentences": [
            {"page": 1, "start": 0, "end": 20, "text": "This document may contain sensitive information."},
            {"page": 1, "start": 21, "end": 45, "text": "You should review it carefully."},
            {"page": 1, "start": 46, "end": 70, "text": "It might be important."},
        ],
    }

    def mock_run_extraction(analysis_id: str, source_file: Path, out_dir: Path):
        extraction_path = out_dir / "extraction.json"
        with extraction_path.open("w", encoding="utf-8") as f:
            json.dump(mock_extraction_data, f)
        return extraction_path

    monkeypatch.setattr("blackletter_api.services.tasks.run_extraction", mock_run_extraction)

    mock_rulepack = Rulepack(
        name="test-rulepack",
        version="v1",
        detectors=[
            Detector(
                id="D001",
                type="lexicon",
                lexicon="weak-language",
                description="Detects weak language.",
            )
        ],
        lexicons={
            "weak-language": Lexicon(
                name="weak-language",
                terms=["may", "might", "could", "should"],
            )
        },
    )

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.load_rulepack", lambda: mock_rulepack
    )

    files = {"file": ("doc.pdf", BytesIO(b"dummy"), "application/pdf")}
    resp = client.post("/api/contracts", files=files)
    job_id = resp.json()["id"]

    fr = client.get("/api/findings", params={"job_id": job_id})
    assert fr.status_code == 200
    findings = fr.json()
    assert isinstance(findings, list)
    assert len(findings) == 3
