"""Tests for Story 4.2 - Coverage Meter"""
import pytest
from blackletter_api.services.coverage import CoverageService, get_coverage_service, compute_analysis_coverage
from blackletter_api.models.schemas import Coverage


def test_coverage_service_initialization():
    """Test coverage service initializes with expected detectors."""
    service = CoverageService()
    
    assert service.total_expected == 8
    assert len(service.expected_detectors) == 8
    assert "A28_3_a_instructions" in service.expected_detectors
    assert "A28_3_h_audits_info" in service.expected_detectors


def test_compute_coverage_complete():
    """Test coverage computation with all detectors present."""
    service = CoverageService()
    analysis_id = "test_analysis_123"
    
    # Mock findings with all 8 detectors
    findings = [
        {"detector_id": "A28_3_a_instructions", "verdict": "pass"},
        {"detector_id": "A28_3_b_confidentiality", "verdict": "weak"},
        {"detector_id": "A28_3_c_security", "verdict": "pass"},
        {"detector_id": "A28_3_d_subprocessors", "verdict": "missing"},
        {"detector_id": "A28_3_e_dsar_assist", "verdict": "pass"},
        {"detector_id": "A28_3_f_breach_notice", "verdict": "needs_review"},
        {"detector_id": "A28_3_g_return_delete", "verdict": "pass"},
        {"detector_id": "A28_3_h_audits_info", "verdict": "weak"},
    ]
    
    coverage = service.compute_coverage(analysis_id, findings)
    
    assert coverage.present == 8
    assert coverage.total == 8
    assert coverage.percentage == 100.0
    assert coverage.status == "complete"
    assert len(coverage.missing_detectors) == 0


def test_compute_coverage_incomplete():
    """Test coverage computation with some detectors missing."""
    service = CoverageService()
    analysis_id = "test_analysis_456"
    
    # Mock findings with only 5 out of 8 detectors
    findings = [
        {"detector_id": "A28_3_a_instructions", "verdict": "pass"},
        {"detector_id": "A28_3_b_confidentiality", "verdict": "weak"},
        {"detector_id": "A28_3_c_security", "verdict": "pass"},
        {"detector_id": "A28_3_d_subprocessors", "verdict": "missing"},
        {"detector_id": "A28_3_e_dsar_assist", "verdict": "pass"},
        # Missing: f, g, h
    ]
    
    coverage = service.compute_coverage(analysis_id, findings)
    
    assert coverage.present == 5
    assert coverage.total == 8
    assert coverage.percentage == 62.5
    assert coverage.status == "incomplete"
    assert len(coverage.missing_detectors) == 3
    assert "A28_3_f_breach_notice" in coverage.missing_detectors
    assert "A28_3_g_return_delete" in coverage.missing_detectors
    assert "A28_3_h_audits_info" in coverage.missing_detectors


def test_compute_coverage_no_findings():
    """Test coverage computation with no findings."""
    service = CoverageService()
    analysis_id = "test_analysis_789"
    
    findings = []
    
    coverage = service.compute_coverage(analysis_id, findings)
    
    assert coverage.present == 0
    assert coverage.total == 8
    assert coverage.percentage == 0.0
    assert coverage.status == "unknown"
    assert len(coverage.missing_detectors) == 8


def test_compute_coverage_ignores_invalid_verdicts():
    """Test that coverage ignores findings without valid verdicts."""
    service = CoverageService()
    analysis_id = "test_analysis_101"
    
    # Mix of valid and invalid findings
    findings = [
        {"detector_id": "A28_3_a_instructions", "verdict": "pass"},
        {"detector_id": "A28_3_b_confidentiality", "verdict": None},  # Invalid
        {"detector_id": "A28_3_c_security", "verdict": ""},  # Invalid
        {"detector_id": "A28_3_d_subprocessors", "verdict": "invalid_verdict"},  # Invalid
        {"detector_id": "A28_3_e_dsar_assist", "verdict": "weak"},
        {"detector_id": "unknown_detector", "verdict": "pass"},  # Unknown detector
    ]
    
    coverage = service.compute_coverage(analysis_id, findings)
    
    # Only a and e should count
    assert coverage.present == 2
    assert coverage.total == 8
    assert coverage.percentage == 25.0
    assert coverage.status == "incomplete"


def test_compute_coverage_handles_rule_id_field():
    """Test that coverage works with rule_id field instead of detector_id."""
    service = CoverageService()
    analysis_id = "test_analysis_102"
    
    # Use rule_id instead of detector_id
    findings = [
        {"rule_id": "A28_3_a_instructions", "verdict": "pass"},
        {"rule_id": "A28_3_b_confidentiality", "verdict": "weak"},
        {"rule_id": "A28_3_c_security", "verdict": "pass"},
    ]
    
    coverage = service.compute_coverage(analysis_id, findings)
    
    assert coverage.present == 3
    assert coverage.total == 8
    assert coverage.percentage == 37.5
    assert coverage.status == "incomplete"


def test_is_complete_coverage():
    """Test complete coverage checker."""
    service = CoverageService()
    
    complete_coverage = Coverage(present=8, total=8, percentage=100.0, status="complete")
    incomplete_coverage = Coverage(present=5, total=8, percentage=62.5, status="incomplete")
    
    assert service.is_complete_coverage(complete_coverage) is True
    assert service.is_complete_coverage(incomplete_coverage) is False


def test_get_coverage_warnings():
    """Test coverage warning messages."""
    service = CoverageService()
    
    # Unknown status
    unknown_coverage = Coverage(
        present=0, total=8, percentage=0.0, status="unknown",
        missing_detectors=["A28_3_a_instructions", "A28_3_b_confidentiality"]
    )
    warnings = service.get_coverage_warnings(unknown_coverage)
    assert "No detector results found" in warnings[0]
    
    # Incomplete status
    incomplete_coverage = Coverage(
        present=5, total=8, percentage=62.5, status="incomplete",
        missing_detectors=["A28_3_f_breach_notice", "A28_3_g_return_delete", "A28_3_h_audits_info"]
    )
    warnings = service.get_coverage_warnings(incomplete_coverage)
    assert "3 detector(s) missing" in warnings[0]


def test_get_coverage_warnings_many_missing():
    """Test coverage warnings with many missing detectors."""
    service = CoverageService()
    
    # Many missing detectors
    incomplete_coverage = Coverage(
        present=2, total=8, percentage=25.0, status="incomplete",
        missing_detectors=[
            "A28_3_c_security", "A28_3_d_subprocessors", "A28_3_e_dsar_assist",
            "A28_3_f_breach_notice", "A28_3_g_return_delete", "A28_3_h_audits_info"
        ]
    )
    warnings = service.get_coverage_warnings(incomplete_coverage)
    assert "6 detector(s) missing" in warnings[0]
    assert "... and 3 more" in warnings[1]


def test_compute_analysis_coverage_convenience_function():
    """Test the convenience function for computing coverage."""
    analysis_id = "test_analysis_999"
    findings = [
        {"detector_id": "A28_3_a_instructions", "verdict": "pass"},
        {"detector_id": "A28_3_b_confidentiality", "verdict": "weak"},
    ]
    
    coverage = compute_analysis_coverage(analysis_id, findings)
    
    assert isinstance(coverage, Coverage)
    assert coverage.present == 2
    assert coverage.total == 8
    assert coverage.percentage == 25.0


def test_get_coverage_service_singleton():
    """Test that get_coverage_service returns singleton instance."""
    service1 = get_coverage_service()
    service2 = get_coverage_service()
    
    assert service1 is service2
    assert isinstance(service1, CoverageService)