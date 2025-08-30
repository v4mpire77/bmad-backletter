from __future__ import annotations

import json
import uuid
from pathlib import Path

from blackletter_api.services.detector_runner import run_detectors
from blackletter_api.services.rulepack_loader import Rulepack, Detector, Lexicon


def test_run_detectors_generates_findings_and_applies_weak_language(tmp_path: Path, monkeypatch):
    """Verify that run_detectors generates findings and applies weak language post-processing."""
    analysis_id = str(uuid.uuid4())
    
    analysis_dir_temp = tmp_path / analysis_id
    analysis_dir_temp.mkdir()

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.analysis_dir",
        lambda aid: analysis_dir_temp
    )

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

    # Create a dummy extraction.json with sentences, some containing weak language terms
    dummy_extraction = {
        "text_path": "extracted.txt",
        "page_map": [
            {"page": 1, "start": 0, "end": 100}
        ],
        "sentences": [
            {"page": 1, "start": 0, "end": 20, "text": "This is a test sentence."},
            {"page": 1, "start": 21, "end": 45, "text": "This might be a weak sentence."},
            {"page": 1, "start": 46, "end": 70, "text": "Another sentence could be here."},
            {"page": 1, "start": 71, "end": 95, "text": "Final sentence with no weak words."}
        ]
    }
    extraction_path = analysis_dir_temp / "extraction.json"
    with extraction_path.open("w") as f:
        json.dump(dummy_extraction, f)

    run_detectors(analysis_id, str(extraction_path))

    findings_path = analysis_dir_temp / "findings.json"
    assert findings_path.exists()

    with findings_path.open("r") as f:
        findings = json.load(f)
    
    # Expect 2 findings for sentences with weak words
    assert len(findings) == 2

    # Check the first finding (might) — snippet should be an evidence window containing the sentence
    finding1 = findings[0]
    assert finding1["detector_id"] == "D001"
    assert finding1["rule_id"] == "D001"
    assert "might" in finding1["snippet"].lower()
    assert len(finding1["snippet"]) >= len("This might be a weak sentence.")
    assert finding1["verdict"] == "weak"  # Should be downgraded by post-processor

    # Check the second finding (could)
    finding2 = findings[1]
    assert finding2["detector_id"] == "D001"
    assert finding2["rule_id"] == "D001"
    assert "could" in finding2["snippet"].lower()
    assert len(finding2["snippet"]) >= len("Another sentence could be here.")
    assert finding2["verdict"] == "weak"  # Should be downgraded by post-processor
