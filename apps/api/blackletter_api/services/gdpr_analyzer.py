"""
Enhanced GDPR Article 28(3) Analyzer
Integrated from v4mpire77/blackletter for improved processor obligations detection
Context Engineering Framework v2.0.0 Compliant
"""
import re
import logging
from typing import List, Dict, Tuple, Optional, Literal
from datetime import datetime

from ..models.schemas import Finding, Coverage
from .rulepack_loader import load_rulepack

logger = logging.getLogger(__name__)


class EnhancedGDPRAnalyzer:
    """
    Enhanced GDPR Article 28(3) processor obligations analyzer.
    Integrated from v4mpire77/blackletter with improved detection patterns.
    """
    
    def __init__(self):
        """Initialize analyzer with enhanced detection patterns."""
        # Load existing rulepack to maintain compatibility
        try:
            self.rulepack = load_rulepack("art28_v1")
        except Exception as e:
            logger.warning(f"Could not load rulepack: {e}, using enhanced patterns only")
            self.rulepack = None
        
        # Enhanced weak language patterns from upstream
        self.weak_language_patterns = [
            r"may\s+at\s+its?\s+discretion",
            r"commercially\s+reasonable",
            r"within\s+a?\s+reasonable\s+time",
            r"best\s+efforts?",
            r"to\s+the\s+extent\s+practicable",
            r"where\s+feasible",
            r"if\s+possible",
            r"endeavour?\s+to",
            r"attempt\s+to",
            r"use\s+reasonable\s+efforts?",
            r"where\s+appropriate",
            r"as\s+may\s+be\s+necessary",
            r"to\s+the\s+extent\s+permissible"
        ]
        
        # Enhanced Article 28(3) obligation patterns from upstream
        self.enhanced_patterns = {
            "28_3_a": {
                "name": "Processing on documented instructions",
                "strong_patterns": [
                    r"shall\s+(?:only\s+)?process\s+.*\s+in\s+accordance\s+with\s+(?:documented\s+)?instructions",
                    r"documented\s+instructions\s+from\s+(?:the\s+)?controller",
                    r"written\s+instructions\s+(?:of\s+|from\s+)(?:the\s+)?controller",
                    r"strictly\s+in\s+accordance\s+with.*instructions",
                    r"only\s+on\s+documented\s+instructions",
                    r"solely\s+in\s+accordance\s+with.*instructions"
                ],
                "weak_patterns": [
                    r"may\s+process.*as.*deems?\s+appropriate",
                    r"general\s+guidance",
                    r"broad\s+directions",
                    r"reasonable\s+instructions"
                ]
            },
            "28_3_b": {
                "name": "Personnel confidentiality",
                "strong_patterns": [
                    r"persons?\s+authorized\s+to\s+process.*committed.*confidentiality",
                    r"personnel.*confidentiality\s+(?:commitment|obligation|undertaking)",
                    r"staff.*bound\s+by\s+confidentiality",
                    r"employees.*confidentiality\s+agreement",
                    r"authorised\s+persons.*confidentiality"
                ],
                "weak_patterns": [
                    r"appropriate\s+confidentiality",
                    r"reasonable\s+confidentiality\s+measures",
                    r"commercially\s+reasonable.*confidentiality"
                ]
            },
            "28_3_c": {
                "name": "Security measures (Article 32)",
                "strong_patterns": [
                    r"appropriate\s+technical\s+and\s+organizational\s+measures",
                    r"security\s+measures.*article\s+32",
                    r"implement.*security.*article\s+32",
                    r"technical\s+and\s+organizational\s+security\s+measures",
                    r"security\s+measures.*pursuant\s+to\s+article\s+32"
                ],
                "weak_patterns": [
                    r"reasonable\s+security\s+measures",
                    r"commercially\s+reasonable.*security",
                    r"industry\s+standard\s+security",
                    r"appropriate\s+security.*where\s+feasible"
                ]
            },
            "28_3_d": {
                "name": "Sub-processor engagement",
                "strong_patterns": [
                    r"prior\s+(?:written\s+)?authorisation.*sub-?processor",
                    r"written\s+consent.*engage.*sub-?processor",
                    r"shall\s+not\s+engage.*sub-?processor.*without.*authorization",
                    r"prior\s+approval.*sub-?processor",
                    r"specific\s+authorization.*sub-?processor"
                ],
                "weak_patterns": [
                    r"may\s+engage\s+sub-?processors?",
                    r"reasonable\s+notice.*sub-?processor",
                    r"general\s+authorization.*sub-?processor",
                    r"commercially\s+reasonable.*sub-?processor"
                ]
            },
            "28_3_e": {
                "name": "Data subject rights assistance",
                "strong_patterns": [
                    r"assist(?:ance)?\s+(?:the\s+)?controller.*data\s+subject\s+rights",
                    r"taking\s+into\s+account.*nature\s+of\s+processing.*assist",
                    r"provide\s+assistance.*data\s+subject\s+rights",
                    r"cooperate.*controller.*data\s+subject\s+requests"
                ],
                "weak_patterns": [
                    r"reasonable\s+assistance.*data\s+subjects?",
                    r"commercially\s+reasonable.*assistance",
                    r"where\s+feasible.*assist.*data\s+subject"
                ]
            },
            "28_3_f": {
                "name": "Data protection impact assessments",
                "strong_patterns": [
                    r"assist.*controller.*carrying\s+out\s+data\s+protection\s+impact\s+assessments?",
                    r"provide\s+assistance.*(?:DPIA|data\s+protection\s+impact\s+assessment)",
                    r"cooperate.*data\s+protection\s+impact\s+assessment",
                    r"assist.*impact\s+assessment.*article\s+35"
                ],
                "weak_patterns": [
                    r"reasonable\s+assistance.*impact\s+assessment",
                    r"where\s+applicable.*impact\s+assessment",
                    r"to\s+the\s+extent\s+feasible.*DPIA"
                ]
            },
            "28_3_g": {
                "name": "Deletion or return of data",
                "strong_patterns": [
                    r"delete\s+(?:or\s+return\s+)?(?:all\s+)?personal\s+data.*end\s+of.*processing",
                    r"return.*personal\s+data.*controller.*end\s+of\s+processing",
                    r"deletion.*personal\s+data.*termination",
                    r"return\s+or\s+delete.*personal\s+data.*upon\s+termination"
                ],
                "weak_patterns": [
                    r"commercially\s+reasonable.*delete",
                    r"where\s+technically\s+feasible.*delete",
                    r"subject\s+to.*delete.*personal\s+data"
                ]
            },
            "28_3_h": {
                "name": "Audits and information provision",
                "strong_patterns": [
                    r"make\s+available.*information\s+necessary.*demonstrate\s+compliance",
                    r"allow\s+for.*contribute\s+to\s+audits",
                    r"provide.*information.*demonstrate.*compliance.*article\s+28",
                    r"permit.*audits.*inspections.*controller"
                ],
                "weak_patterns": [
                    r"reasonable\s+information.*compliance",
                    r"commercially\s+reasonable.*audit",
                    r"where\s+feasible.*information.*compliance"
                ]
            }
        }
    
    def analyze_document(
        self, 
        text: str, 
        analysis_id: str,
        filename: str = "document.pdf"
    ) -> Tuple[List[Finding], Coverage]:
        """
        Analyze document for GDPR Article 28(3) compliance with enhanced detection.
        
        Returns:
            Tuple of findings list and coverage assessment
        """
        findings = []
        detected_obligations = set()
        
        # Analyze each Article 28(3) obligation
        for obligation_id, patterns in self.enhanced_patterns.items():
            finding = self._analyze_obligation(
                text, obligation_id, patterns, analysis_id, filename
            )
            if finding:
                findings.append(finding)
                if finding.verdict in ["pass", "weak"]:
                    detected_obligations.add(obligation_id)
        
        # Calculate coverage
        coverage = self._calculate_coverage(detected_obligations)
        
        logger.info(f"Enhanced GDPR analysis complete: {len(findings)} findings, "
                   f"{len(detected_obligations)}/8 obligations detected")
        
        return findings, coverage
    
    def _analyze_obligation(
        self,
        text: str,
        obligation_id: str,
        patterns: Dict[str, List[str]],
        analysis_id: str,
        filename: str
    ) -> Optional[Finding]:
        """Analyze a single Article 28(3) obligation."""
        strong_matches = []
        weak_matches = []
        weak_language_found = False
        
        # Check for strong patterns
        for pattern in patterns["strong_patterns"]:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            strong_matches.extend(matches)
        
        # Check for weak patterns
        for pattern in patterns["weak_patterns"]:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            weak_matches.extend(matches)
        
        # Check for weak language in the vicinity of strong matches
        if strong_matches:
            for match in strong_matches:
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 200)
                context = text[start:end]
                
                for weak_pattern in self.weak_language_patterns:
                    if re.search(weak_pattern, context, re.IGNORECASE):
                        weak_language_found = True
                        break
        
        # Determine verdict
        verdict = "missing"
        snippet = ""
        rationale = f"No evidence found for {patterns['name']}"
        confidence = 0.0
        
        if strong_matches:
            if weak_language_found:
                verdict = "weak"
                rationale = f"Found {patterns['name']} but contains qualifying/weak language"
                confidence = 0.7
            else:
                verdict = "pass"
                rationale = f"Clear evidence of {patterns['name']} found"
                confidence = 0.9
            
            # Use the first strong match for the snippet
            match = strong_matches[0]
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            snippet = text[start:end].strip()
            
        elif weak_matches:
            verdict = "weak"
            rationale = f"Weak or qualified language found for {patterns['name']}"
            confidence = 0.5
            
            # Use the first weak match for the snippet
            match = weak_matches[0]
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            snippet = text[start:end].strip()
        
        # Create finding
        return Finding(
            detector_id=obligation_id,
            rule_id=f"art28_v1.{obligation_id}",
            verdict=verdict,
            snippet=snippet,
            page=1,  # Placeholder - would need page mapping
            start=strong_matches[0].start() if strong_matches else (weak_matches[0].start() if weak_matches else 0),
            end=strong_matches[0].end() if strong_matches else (weak_matches[0].end() if weak_matches else 0),
            rationale=rationale,
            confidence=confidence,
            weak_language_detected=weak_language_found
        )
    
    def _calculate_coverage(self, detected_obligations: set) -> Coverage:
        """Calculate GDPR Article 28(3) coverage."""
        total_obligations = 8  # 28(3)(a) through 28(3)(h)
        present = len(detected_obligations)
        percentage = (present / total_obligations) * 100
        
        missing_detectors = []
        all_obligations = set(f"28_3_{chr(97 + i)}" for i in range(8))  # a-h
        for obligation in all_obligations - detected_obligations:
            missing_detectors.append(obligation)
        
        status = "complete" if percentage == 100 else ("incomplete" if percentage > 0 else "unknown")
        
        return Coverage(
            present=present,
            total=total_obligations,
            percentage=percentage,
            missing_detectors=missing_detectors,
            status=status
        )


# Create singleton instance for use across the application
gdpr_analyzer = EnhancedGDPRAnalyzer()