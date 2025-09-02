"""Coverage service for Story 4.2 - Coverage Meter"""
from __future__ import annotations

import logging
from typing import Dict, Any, List, Set
from ..models.schemas import Coverage

logger = logging.getLogger(__name__)

# Expected detectors for Art 28 GDPR requirements (a-h)
EXPECTED_DETECTORS = {
    "A28_3_a_instructions",
    "A28_3_b_confidentiality", 
    "A28_3_c_security",
    "A28_3_d_subprocessors",
    "A28_3_e_dsar_assist",
    "A28_3_f_breach_notice",
    "A28_3_g_return_delete",
    "A28_3_h_audits_info"
}


class CoverageService:
    """Service for computing detector coverage per analysis."""
    
    def __init__(self):
        self.expected_detectors = EXPECTED_DETECTORS
        self.total_expected = len(EXPECTED_DETECTORS)
    
    def compute_coverage(self, analysis_id: str, findings: List[Dict[str, Any]]) -> Coverage:
        """
        Compute coverage for Story 4.2.
        
        Coverage per analysis: all eight detectors present with a verdict.
        
        Args:
            analysis_id: Analysis ID
            findings: List of detection findings
            
        Returns:
            Coverage object with present/total counts and status
        """
        try:
            # Extract detector IDs that have verdicts
            present_detectors = set()
            
            for finding in findings:
                detector_id = finding.get('detector_id') or finding.get('rule_id')
                verdict = finding.get('verdict')
                
                # Only count detectors with actual verdicts
                if detector_id and verdict and verdict in ['pass', 'weak', 'missing', 'needs_review']:
                    present_detectors.add(detector_id)
            
            # Calculate coverage
            present_count = len(present_detectors & self.expected_detectors)
            missing_detectors = list(self.expected_detectors - present_detectors)
            percentage = round((present_count / self.total_expected) * 100, 2)
            
            # Determine status
            if present_count == self.total_expected:
                status = "complete"
            elif present_count > 0:
                status = "incomplete"
            else:
                status = "unknown"
            
            logger.info(
                f"Computed coverage for analysis {analysis_id}: "
                f"{present_count}/{self.total_expected} ({percentage}%)"
            )
            
            return Coverage(
                present=present_count,
                total=self.total_expected,
                percentage=percentage,
                missing_detectors=missing_detectors,
                status=status
            )
            
        except Exception as e:
            logger.error(f"Failed to compute coverage for {analysis_id}: {e}")
            return Coverage(
                present=0,
                total=self.total_expected,
                percentage=0.0,
                missing_detectors=list(self.expected_detectors),
                status="unknown"
            )
    
    def get_expected_detectors(self) -> Set[str]:
        """Get the set of expected detector IDs."""
        return self.expected_detectors.copy()
    
    def is_complete_coverage(self, coverage: Coverage) -> bool:
        """Check if coverage is complete (all detectors present)."""
        return coverage.present == coverage.total
    
    def get_coverage_warnings(self, coverage: Coverage) -> List[str]:
        """Get warning messages for incomplete coverage."""
        warnings = []
        
        if coverage.status == "unknown":
            warnings.append("No detector results found")
        elif coverage.status == "incomplete":
            missing_count = len(coverage.missing_detectors)
            warnings.append(f"{missing_count} detector(s) missing: {', '.join(coverage.missing_detectors[:3])}")
            if missing_count > 3:
                warnings.append(f"... and {missing_count - 3} more")
        
        return warnings


# Global instance
_coverage_service_instance: CoverageService = None


def get_coverage_service() -> CoverageService:
    """Get the global coverage service instance."""
    global _coverage_service_instance
    if _coverage_service_instance is None:
        _coverage_service_instance = CoverageService()
    return _coverage_service_instance


def compute_analysis_coverage(analysis_id: str, findings: List[Dict[str, Any]]) -> Coverage:
    """
    Convenience function to compute coverage for an analysis.
    
    Args:
        analysis_id: Analysis ID
        findings: List of detection findings
        
    Returns:
        Coverage object
    """
    service = get_coverage_service()
    return service.compute_coverage(analysis_id, findings)