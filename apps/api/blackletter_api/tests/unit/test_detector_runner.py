from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from blackletter_api.services.detector_runner import run_detectors
import blackletter_api.services.rulepack_loader as rl
from blackletter_api.services.weak_lexicon import (
    get_weak_terms_with_metadata,
    get_counter_anchors,
)

rl.Any = Any  # Ensure forward references are resolved
rl.Lexicon.model_rebuild()
rl.Detector.model_rebuild()
rl.Rulepack.model_rebuild()

Rulepack = rl.Rulepack
Detector = rl.Detector
Lexicon = rl.Lexicon


def test_run_detectors_generates_findings_and_applies_weak_language(tmp_path: Path, monkeypatch):
    """Verify that run_detectors generates findings and applies weak language post-processing."""
    analysis_id = str(uuid.uuid4())
    
    analysis_dir_temp = tmp_path / analysis_id
    analysis_dir_temp.mkdir()

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.analysis_dir",
        lambda aid: analysis_dir_temp
    )

    class DummyLedger:
        def add_tokens(self, *args, **kwargs):
            return False, None

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.get_token_ledger",
        lambda: DummyLedger(),
    )
    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.should_apply_token_capping",
        lambda: False,
    )
    get_weak_terms_with_metadata.cache_clear()
    get_counter_anchors.cache_clear()

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
            "weak_language": Lexicon(
                name="weak_language",
                terms=["may", "might", "could", "should"]
            )
        }
    )
    monkeypatch.setattr("blackletter_api.services.detector_runner.load_rulepack", lambda: mock_rulepack)
    monkeypatch.setattr("blackletter_api.services.weak_lexicon.load_rulepack", lambda: mock_rulepack)

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

    # Check the first finding (might)
    finding1 = findings[0]
    assert finding1["detector_id"] == "D001"
    assert finding1["rule_id"] == "D001"
    assert finding1["snippet"] == "This might be a weak sentence."
    assert finding1["verdict"] == "weak" # Should be downgraded by post-processor

    # Check the second finding (could)
    finding2 = findings[1]
    assert finding2["detector_id"] == "D001"
    assert finding2["rule_id"] == "D001"
    assert finding2["snippet"] == "Another sentence could be here."
    assert finding2["verdict"] == "weak" # Should be downgraded by post-processor


def test_run_detectors_handles_regex_detectors(tmp_path: Path, monkeypatch):
    """Ensure regex-based detectors generate findings and persist them."""
    analysis_id = str(uuid.uuid4())

    analysis_dir_temp = tmp_path / analysis_id
    analysis_dir_temp.mkdir()

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.analysis_dir",
        lambda aid: analysis_dir_temp
    )

    class DummyLedger:
        def add_tokens(self, *args, **kwargs):
            return False, None

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.get_token_ledger",
        lambda: DummyLedger(),
    )
    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.should_apply_token_capping",
        lambda: False,
    )
    get_weak_terms_with_metadata.cache_clear()
    get_counter_anchors.cache_clear()

    mock_rulepack = Rulepack(
        name="regex-pack",
        version="v1",
        detectors=[
            Detector(
                id="R001",
                type="regex",
                pattern=r"foo\d+",
                description="Matches foo followed by digits",
            )
        ],
        lexicons={}
    )

    monkeypatch.setattr("blackletter_api.services.detector_runner.load_rulepack", lambda: mock_rulepack)
    monkeypatch.setattr("blackletter_api.services.weak_lexicon.load_rulepack", lambda: mock_rulepack)

    dummy_extraction = {
        "text_path": "extracted.txt",
        "page_map": [{"page": 1, "start": 0, "end": 50}],
        "sentences": [
            {"page": 1, "start": 0, "end": 25, "text": "This sentence has FoO123 pattern."},
            {"page": 1, "start": 26, "end": 50, "text": "Nothing to see here."}
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

    assert len(findings) == 1
    finding = findings[0]
    assert finding["detector_id"] == "R001"
    assert finding["rule_id"] == "R001"
    assert finding["snippet"] == "This sentence has FoO123 pattern."
    assert finding["verdict"] == "pass"


def test_run_detectors_regex_no_match(tmp_path: Path, monkeypatch):
    """Regex detector with no matches should yield no findings."""
    analysis_id = str(uuid.uuid4())

    analysis_dir_temp = tmp_path / analysis_id
    analysis_dir_temp.mkdir()

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.analysis_dir",
        lambda aid: analysis_dir_temp,
    )

    class DummyLedger:
        def add_tokens(self, *args, **kwargs):
            return False, None

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.get_token_ledger",
        lambda: DummyLedger(),
    )
    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.should_apply_token_capping",
        lambda: False,
    )
    get_weak_terms_with_metadata.cache_clear()
    get_counter_anchors.cache_clear()

    mock_rulepack = Rulepack(
        name="regex-pack",
        version="v1",
        detectors=[
            Detector(
                id="R002",
                type="regex",
                pattern=r"bar\d+",
                description="Matches bar followed by digits",
            )
        ],
        lexicons={},
    )

    monkeypatch.setattr("blackletter_api.services.detector_runner.load_rulepack", lambda: mock_rulepack)
    monkeypatch.setattr("blackletter_api.services.weak_lexicon.load_rulepack", lambda: mock_rulepack)

    dummy_extraction = {
        "text_path": "extracted.txt",
        "page_map": [{"page": 1, "start": 0, "end": 50}],
        "sentences": [
            {"page": 1, "start": 0, "end": 25, "text": "This sentence has FoO123 pattern."},
            {"page": 1, "start": 26, "end": 50, "text": "Nothing to see here."},
        ],
    }

    extraction_path = analysis_dir_temp / "extraction.json"
    with extraction_path.open("w") as f:
        json.dump(dummy_extraction, f)

    run_detectors(analysis_id, str(extraction_path))

    findings_path = analysis_dir_temp / "findings.json"
    assert findings_path.exists()

    with findings_path.open("r") as f:
        findings = json.load(f)

    assert findings == []


def test_run_detectors_regex_malformed_pattern(tmp_path: Path, monkeypatch):
    """Malformed regex patterns should be skipped without error."""
    analysis_id = str(uuid.uuid4())

    analysis_dir_temp = tmp_path / analysis_id
    analysis_dir_temp.mkdir()

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.analysis_dir",
        lambda aid: analysis_dir_temp,
    )

    class DummyLedger:
        def add_tokens(self, *args, **kwargs):
            return False, None

    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.get_token_ledger",
        lambda: DummyLedger(),
    )
    monkeypatch.setattr(
        "blackletter_api.services.detector_runner.should_apply_token_capping",
        lambda: False,
    )
    get_weak_terms_with_metadata.cache_clear()
    get_counter_anchors.cache_clear()

    mock_rulepack = Rulepack(
        name="regex-pack",
        version="v1",
        detectors=[
            Detector(
                id="R003",
                type="regex",
                pattern=r"foo(",  # malformed regex
                description="Malformed pattern",
            )
        ],
        lexicons={},
    )

    monkeypatch.setattr("blackletter_api.services.detector_runner.load_rulepack", lambda: mock_rulepack)
    monkeypatch.setattr("blackletter_api.services.weak_lexicon.load_rulepack", lambda: mock_rulepack)

    dummy_extraction = {
        "text_path": "extracted.txt",
        "page_map": [{"page": 1, "start": 0, "end": 50}],
        "sentences": [
            {"page": 1, "start": 0, "end": 25, "text": "This sentence has FoO123 pattern."},
            {"page": 1, "start": 26, "end": 50, "text": "Nothing to see here."},
        ],
    }

    extraction_path = analysis_dir_temp / "extraction.json"
    with extraction_path.open("w") as f:
        json.dump(dummy_extraction, f)

    run_detectors(analysis_id, str(extraction_path))

    findings_path = analysis_dir_temp / "findings.json"
    assert findings_path.exists()

    with findings_path.open("r") as f:
        findings = json.load(f)

    assert findings == []
