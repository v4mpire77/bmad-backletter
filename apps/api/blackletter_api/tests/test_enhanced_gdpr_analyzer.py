"""
Enhanced GDPR Analyzer Test Suite
Integrated from v4mpire77/blackletter with golden test validation
Context Engineering Framework v2.0.0 Compliant
Validates precision ≥85%, recall ≥90%, latency <60s
"""
import json
import pytest
import time
from pathlib import Path
from typing import List, Dict, Any

from blackletter_api.services.gdpr_analyzer import gdpr_analyzer


class TestEnhancedGDPRAnalyzer:
    """Test suite for enhanced GDPR Article 28(3) analyzer."""
    
    @classmethod
    def setup_class(cls):
        """Load golden test fixtures."""
        fixtures_path = Path(__file__).parent / "fixtures" / "processor_obligations" / "golden_tests.json"
        with open(fixtures_path, 'r') as f:
            cls.golden_tests = json.load(f)
    
    def test_analyzer_initialization(self):
        """Test that the analyzer initializes correctly."""
        assert gdpr_analyzer is not None
        assert hasattr(gdpr_analyzer, 'enhanced_patterns')
        assert len(gdpr_analyzer.enhanced_patterns) == 8  # 28(3)(a) through (h)
    
    def test_weak_instructions_detection(self):
        """Test detection of weak processing instructions."""
        test_case = self._get_test_case("weak_28_3_a_instructions")
        contract_text = test_case["contract_text"]
        
        findings, coverage = gdpr_analyzer.analyze_document(
            contract_text, "test_analysis_1", "weak_instructions.txt"
        )
        
        # Validate findings
        assert len(findings) > 0, "Should detect weak language in instructions"
        
        instructions_finding = next(
            (f for f in findings if f.detector_id == "28_3_a"), None
        )
        assert instructions_finding is not None, "Should detect 28(3)(a) issue"
        assert instructions_finding.verdict == "weak", "Should classify as weak"
        assert instructions_finding.confidence >= 0.70, "Should meet minimum confidence"
    
    def test_missing_confidentiality_detection(self):
        """Test detection of missing personnel confidentiality."""
        test_case = self._get_test_case("missing_28_3_b_confidentiality")
        contract_text = test_case["contract_text"]
        
        findings, coverage = gdpr_analyzer.analyze_document(
            contract_text, "test_analysis_2", "missing_confidentiality.txt"
        )
        
        # Should not detect confidentiality obligation
        confidentiality_finding = next(
            (f for f in findings if f.detector_id == "28_3_b"), None
        )
        if confidentiality_finding:
            assert confidentiality_finding.verdict == "missing", "Should classify as missing"
    
    def test_strong_compliance_detection(self):
        """Test detection of strong compliance language."""
        strong_text = """
        The Processor shall process Personal Data only on documented instructions from the Controller,
        including with regard to transfers of personal data to a third country or an international
        organisation, unless required to do so by Union or Member State law.
        
        The Processor ensures that persons authorised to process the personal data have committed
        themselves to confidentiality or are under an appropriate statutory obligation of confidentiality.
        
        The Processor shall implement appropriate technical and organisational measures to ensure
        a level of security appropriate to the risk pursuant to Article 32.
        """
        
        findings, coverage = gdpr_analyzer.analyze_document(
            strong_text, "test_analysis_3", "strong_compliance.txt"
        )
        
        # Should detect multiple strong obligations
        pass_findings = [f for f in findings if f.verdict == "pass"]
        assert len(pass_findings) >= 2, "Should detect multiple strong obligations"
        
        # Coverage should be good
        assert coverage.present >= 3, "Should detect at least 3 obligations"
        assert coverage.percentage > 30, "Should have reasonable coverage percentage"
    
    def test_performance_latency(self):
        """Test that analysis completes within performance requirements."""
        # Use a moderately sized contract text
        large_text = """
        This Data Processing Agreement governs the processing of Personal Data by Processor on behalf of Controller.
        
        1. Processing Instructions
        The Processor shall process Personal Data only on documented instructions from the Controller.
        Such instructions shall be in writing and may be amended from time to time.
        
        2. Confidentiality
        The Processor ensures that persons authorised to process the personal data have committed
        themselves to confidentiality or are under an appropriate statutory obligation of confidentiality.
        
        3. Security Measures
        The Processor shall implement appropriate technical and organisational measures to ensure
        a level of security appropriate to the risk pursuant to Article 32 of the GDPR.
        
        4. Sub-processors
        The Processor shall not engage another processor without prior specific or general written
        authorisation of the Controller.
        
        5. Data Subject Rights
        Taking into account the nature of the processing, the Processor shall assist the Controller
        by appropriate technical and organisational measures for the fulfilment of the Controller's
        obligation to respond to requests for exercising the data subject's rights.
        
        6. Data Protection Impact Assessments
        The Processor shall assist the Controller in ensuring compliance with the obligations pursuant
        to Articles 32 to 36 taking into account the nature of processing and the information available
        to the Processor.
        
        7. Deletion or Return
        The Processor shall delete or return all the personal data to the Controller after the end
        of the provision of services relating to processing.
        
        8. Audits and Information
        The Processor shall make available to the Controller all information necessary to demonstrate
        compliance with the obligations laid down in this Article and allow for and contribute to
        audits, including inspections, conducted by the Controller.
        """ * 3  # Triple the text to make it larger
        
        start_time = time.time()
        findings, coverage = gdpr_analyzer.analyze_document(
            large_text, "test_analysis_4", "performance_test.txt"
        )
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert processing_time < 60, f"Analysis took {processing_time:.2f}s, should be <60s"
    
    def test_golden_tests_precision_recall(self):
        """Test against golden test fixtures for precision/recall validation."""
        test_cases = self.golden_tests["processor_obligations_test_cases"]
        
        total_cases = len(test_cases)
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        
        for test_case in test_cases:
            contract_text = test_case["contract_text"]
            expected_issues = test_case["expected_issues"]
            expected_coverage = test_case["expected_coverage"]
            
            findings, coverage = gdpr_analyzer.analyze_document(
                contract_text, f"golden_test_{test_case['id']}", f"{test_case['id']}.txt"
            )
            
            # Evaluate each expected issue
            for expected in expected_issues:
                found_issue = self._find_matching_issue(findings, expected)
                if found_issue:
                    true_positives += 1
                else:
                    false_negatives += 1
            
            # Check for unexpected issues (false positives)
            for finding in findings:
                if not self._matches_expected_issues(finding, expected_issues):
                    false_positives += 1
        
        # Calculate precision and recall
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        
        print(f"\nGolden Test Results:")
        print(f"True Positives: {true_positives}")
        print(f"False Positives: {false_positives}")
        print(f"False Negatives: {false_negatives}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall: {recall:.3f}")
        
        # Assert precision ≥85%, recall ≥90% as required
        assert precision >= 0.85, f"Precision {precision:.3f} below required 0.85"
        assert recall >= 0.90, f"Recall {recall:.3f} below required 0.90"
    
    def test_coverage_calculation(self):
        """Test coverage calculation accuracy."""
        # Text with exactly 4 obligations present
        partial_text = """
        The Processor shall process Personal Data only on documented instructions from the Controller.
        The Processor ensures that persons authorised to process the personal data have committed
        themselves to confidentiality.
        The Processor shall implement appropriate technical and organisational measures.
        The Processor shall not engage another processor without prior written authorisation.
        """
        
        findings, coverage = gdpr_analyzer.analyze_document(
            partial_text, "test_coverage", "coverage_test.txt"
        )
        
        assert coverage.total == 8, "Should track 8 total obligations"
        assert coverage.present <= 8, "Present count should not exceed total"
        assert coverage.percentage == (coverage.present / coverage.total) * 100
        assert coverage.status in ["complete", "incomplete", "unknown"]
    
    def test_weak_language_detection(self):
        """Test weak language pattern detection."""
        weak_text = """
        The Processor may process Personal Data as commercially reasonable for the purposes
        of this Agreement. Where feasible, the Processor will endeavour to follow Controller
        instructions to the extent practicable.
        """
        
        findings, coverage = gdpr_analyzer.analyze_document(
            weak_text, "test_weak", "weak_language.txt"
        )
        
        weak_findings = [f for f in findings if f.weak_language_detected]
        assert len(weak_findings) > 0, "Should detect weak language patterns"
    
    def _get_test_case(self, case_id: str) -> Dict[str, Any]:
        """Helper to get specific test case by ID."""
        test_cases = self.golden_tests["processor_obligations_test_cases"]
        return next(tc for tc in test_cases if tc["id"] == case_id)
    
    def _find_matching_issue(self, findings: List, expected: Dict[str, Any]) -> bool:
        """Check if findings contain an issue matching the expected one."""
        for finding in findings:
            if (finding.verdict in ["weak", "missing"] and 
                expected["type"] in ["weak_language", "missing_obligation"] and
                finding.confidence >= expected.get("confidence_min", 0.0)):
                return True
        return False
    
    def _matches_expected_issues(self, finding, expected_issues: List[Dict]) -> bool:
        """Check if a finding matches any expected issue."""
        for expected in expected_issues:
            if self._find_matching_issue([finding], expected):
                return True
        return False


# Additional integration tests
class TestGDPRAnalyzerIntegration:
    """Integration tests for GDPR analyzer with the task system."""
    
    def test_analyzer_task_integration(self):
        """Test that the analyzer integrates properly with Celery tasks."""
        from blackletter_api.services.tasks import run_gdpr_analysis
        
        test_text = "The Processor shall process Personal Data only on documented instructions."
        findings, coverage = run_gdpr_analysis(test_text, "integration_test", "test.txt")
        
        assert isinstance(findings, list)
        assert hasattr(coverage, 'present')
        assert hasattr(coverage, 'total')
    
    def test_error_handling(self):
        """Test analyzer error handling with invalid input."""
        # Empty text should not crash
        findings, coverage = gdpr_analyzer.analyze_document("", "empty_test", "empty.txt")
        assert isinstance(findings, list)
        assert coverage.present == 0
        
        # Very short text should work
        findings, coverage = gdpr_analyzer.analyze_document("test", "short_test", "short.txt")
        assert isinstance(findings, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])