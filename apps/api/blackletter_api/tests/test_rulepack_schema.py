"""Test for rulepack schema validation."""
import pytest
from apps.api.blackletter_api.models.rulepack_schema import validate_rulepack, RulepackValidationError


def test_valid_rulepack():
    """Test that a valid rulepack passes validation."""
    data = {
        "meta": {
            "pack_id": "gdpr_art28",
            "version": "1.0.0",
            "evidence_window_sentences": 3,
            "verdicts": ["pass", "weak", "missing", "needs_review"],
            "tokenizer": "sentence"
        },
        "shared_lexicon": {
            "hedges": ["may", "might", "could"],
            "strong": ["must", "shall", "required"]
        },
        "Detectors": [
            {
                "id": "data_controller_obligations",
                "anchors_any": ["data controller", "controller"],
                "weak_nearby": {
                    "any": ["@hedges"]
                }
            }
        ]
    }
    
    # This should not raise an exception
    rulepack = validate_rulepack(data)
    assert rulepack.meta.pack_id == "gdpr_art28"
    assert rulepack.meta.version == "1.0.0"


def test_invalid_version():
    """Test that invalid version format fails validation."""
    data = {
        "meta": {
            "pack_id": "gdpr_art28",
            "version": "1.0",  # Missing patch version
            "evidence_window_sentences": 3,
            "verdicts": ["pass", "weak", "missing", "needs_review"],
            "tokenizer": "sentence"
        },
        "shared_lexicon": {},
        "Detectors": [
            {
                "id": "data_controller_obligations",
                "anchors_any": ["data controller", "controller"]
            }
        ]
    }
    
    with pytest.raises(RulepackValidationError) as exc_info:
        validate_rulepack(data)
    
    assert "Invalid semantic version format" in str(exc_info.value)
    assert exc_info.value.field == "meta.version"


def test_empty_detector_id():
    """Test that empty detector ID fails validation."""
    data = {
        "meta": {
            "pack_id": "gdpr_art28",
            "version": "1.0.0",
            "evidence_window_sentences": 3,
            "verdicts": ["pass", "weak", "missing", "needs_review"],
            "tokenizer": "sentence"
        },
        "shared_lexicon": {},
        "Detectors": [
            {
                "id": "",  # Empty ID
                "anchors_any": ["data controller", "controller"]
            }
        ]
    }
    
    with pytest.raises(RulepackValidationError) as exc_info:
        validate_rulepack(data)
    
    assert "Detector ID cannot be empty" in str(exc_info.value)
    assert exc_info.value.field == "detector.id"


def test_duplicate_detector_ids():
    """Test that duplicate detector IDs fail validation."""
    data = {
        "meta": {
            "pack_id": "gdpr_art28",
            "version": "1.0.0",
            "evidence_window_sentences": 3,
            "verdicts": ["pass", "weak", "missing", "needs_review"],
            "tokenizer": "sentence"
        },
        "shared_lexicon": {},
        "Detectors": [
            {
                "id": "data_controller_obligations",
                "anchors_any": ["data controller", "controller"]
            },
            {
                "id": "data_controller_obligations",  # Duplicate ID
                "anchors_any": ["processor", "sub-processor"]
            }
        ]
    }
    
    with pytest.raises(RulepackValidationError) as exc_info:
        validate_rulepack(data)
    
    assert "Duplicate detector IDs found" in str(exc_info.value)
    assert exc_info.value.field == "Detectors"


def test_invalid_pattern():
    """Test that invalid patterns fail validation."""
    data = {
        "meta": {
            "pack_id": "gdpr_art28",
            "version": "1.0.0",
            "evidence_window_sentences": 3,
            "verdicts": ["pass", "weak", "missing", "needs_review"],
            "tokenizer": "sentence"
        },
        "shared_lexicon": {},
        "Detectors": [
            {
                "id": "data_controller_obligations",
                "anchors_any": ["data controller", ""]  # Empty pattern
            }
        ]
    }
    
    with pytest.raises(RulepackValidationError) as exc_info:
        validate_rulepack(data)
    
    assert "Pattern cannot be empty or whitespace only" in str(exc_info.value)
    assert "detector.anchors_any" in str(exc_info.value.field)