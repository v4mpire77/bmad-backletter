from __future__ import annotations

import json
import uuid
from pathlib import Path

from blackletter_api.services.detector_runner import run_detectors


def test_run_detectors_creates_findings_file(tmp_path: Path, monkeypatch):
    """Verify that run_detectors creates a findings.json file."""
    analysis_id = str(uuid.uuid4())
    
    # The detector runner expects the analysis dir to exist
    analysis_dir_temp = tmp_path / analysis_id
    analysis_dir_temp.mkdir()

    # Monkeypatch the storage function to use our temp directory
    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.analysis_dir",
        lambda aid: analysis_dir_temp
    )

    # Create a dummy extraction.json for the runner to read
    dummy_extraction = {
        "text_path": "extracted.txt",
        "page_map": [],
        "sentences": []
    }
    extraction_path = analysis_dir_temp / "extraction.json"
    with extraction_path.open("w") as f:
        json.dump(dummy_extraction, f)

    # Run the detector
    run_detectors(analysis_id, str(extraction_path))

    # Check that findings.json was created
    findings_path = analysis_dir_temp / "findings.json"
    assert findings_path.exists()

    # Check the content of the findings
    with findings_path.open("r") as f:
        findings = json.load(f)
    
    assert len(findings) == 1
    finding = findings[0]
    assert finding["detector_id"] == "D001"
    # The dummy text "This is a sample text." has no weak words
    assert finding["verdict"] == "pass"
