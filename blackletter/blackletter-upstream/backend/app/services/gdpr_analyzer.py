"""
Blackletter GDPR Processor - GDPR Article 28(3) Analyzer
Context Engineering Framework v2.0.0 Compliant
Implements processor obligations detection per build guide specifications
"""
import re
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime

from app.models.schemas import (
    Issue, Coverage, SeverityEnum, IssueTypeEnum, CoverageStatusEnum,
    create_issue, create_coverage
)

logger = logging.getLogger(__name__)


class GDPRArticle28Analyzer:
    """
    GDPR Article 28(3) processor obligations analyzer.
    Detects presence, absence, and weakness of required processor obligations.
    """
    
    def __init__(self):
        """Initialize analyzer with detection patterns."""
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
            r"use\s+reasonable\s+efforts?"
        ]
        
        # Article 28(3) obligation patterns
        self.obligation_patterns = {
            "28_3_a": {
                "name": "Processing on documented instructions",
                "strong_patterns": [
                    r"shall\s+(?:only\s+)?process\s+.*\s+in\s+accordance\s+with\s+(?:documented\s+)?instructions",
                    r"documented\s+instructions\s+from\s+(?:the\s+)?controller",
                    r"written\s+instructions\s+(?:of\s+|from\s+)(?:the\s+)?controller",
                    r"strictly\s+in\s+accordance\s+with.*instructions"
                ],
                "weak_patterns": [
                    r"may\s+process.*as.*deems?\s+appropriate",
                    r"general\s+guidance",
                    r"broad\s+directions"
                ]
            },
            "28_3_b": {
                "name": "Personnel confidentiality",
                "strong_patterns": [
                    r"persons?\s+authorized\s+to\s+process.*committed.*confidentiality",
                    r"personnel.*confidentiality\s+(?:commitment|obligation|undertaking)",
                    r"staff.*bound\s+by\s+confidentiality",
                    r"employees.*confidentiality\s+agreement"
                ],
                "weak_patterns": [
                    r"appropriate\s+confidentiality",
                    r"reasonable\s+confidentiality\s+measures"
                ]
            },
            "28_3_c": {
                "name": "Security measures (Article 32)",
                "strong_patterns": [
                    r"appropriate\s+technical\s+and\s+organizational\s+measures",
                    r"security\s+measures.*article\s+32",
                    r"implement.*security.*article\s+32",
                    r"technical\s+and\s+organizational\s+security\s+measures"
                ],
                "weak_patterns": [
                    r"reasonable\s+security\s+measures",
                    r"commercially\s+reasonable.*security",
                    r"industry\s+standard\s+security"
                ]
            },
            "28_3_d": {
                "name": "Sub-processor engagement",
                "strong_patterns": [
                    r"prior\s+(?:written\s+)?authorisation.*sub-?processor",
                    r"written\s+consent.*engage.*sub-?processor",
                    r"shall\s+not\s+engage.*sub-?processor.*without.*authorization",
                    r"prior\s+approval.*sub-?processor"
                ],
                "weak_patterns": [
                    r"may\s+engage\s+sub-?processors?",
                    r"reasonable\s+notice.*sub-?processor",
                    r"general\s+authorization.*sub-?processor"
                ]
            },
            "28_3_e": {
                "name": "Data subject rights assistance",
                "strong_patterns": [
                    r"assist(?:ance)?\s+(?:the\s+)?controller.*data\s+subject\s+rights",
                    r"support.*controller.*rights\s+requests?",
                    r"assist.*exercis(?:e|ing)\s+(?:of\s+)?(?:their\s+)?rights",
                    r"cooperation.*data\s+subject\s+requests?"
                ],
                "weak_patterns": [
                    r"reasonable\s+assistance.*data\s+subject",
                    r"cooperate.*extent\s+possible.*rights"
                ]
            },
            "28_3_f": {
                "name": "Breach notification",
                "strong_patterns": [
                    r"notify.*controller.*personal\s+data\s+breach",
                    r"inform.*controller.*breach.*(?:24|72)\s+hours?",
                    r"immediately\s+(?:notify|inform).*breach",
                    r"without\s+undue\s+delay.*notify.*breach"
                ],
                "weak_patterns": [
                    r"notify.*controller.*breach.*reasonable\s+time",
                    r"inform.*controller.*breach.*practicable"
                ]
            },
            "28_3_g": {
                "name": "Deletion/return of data",
                "strong_patterns": [
                    r"delete\s+or\s+return.*personal\s+data",
                    r"deletion.*return.*personal\s+data.*end\s+of.*processing",
                    r"return\s+or\s+delete.*termination",
                    r"secure\s+deletion.*personal\s+data"
                ],
                "weak_patterns": [
                    r"may\s+(?:delete|return).*personal\s+data",
                    r"reasonable\s+efforts.*delete.*personal\s+data"
                ]
            },
            "28_3_h": {
                "name": "Audit and inspection rights",
                "strong_patterns": [
                    r"audit(?:s|ing)?.*inspection(?:s)?",
                    r"demonstrate\s+compliance.*(?:audit|inspection)",
                    r"allow(?:s)?\s+(?:for\s+)?audit(?:s|ing)?",
                    r"right\s+to\s+audit"
                ],
                "weak_patterns": [
                    r"reasonable\s+access.*audit",
                    r"commercially\s+reasonable.*inspection"
                ]
            }
        }
    
    def analyze_processor_obligations(self, text: str, doc_id: str = "document") -> Tuple[List[Issue], List[Coverage]]:
        """
        Analyze contract text for GDPR Article 28(3) processor obligations.
        
        Args:
            text: Contract text to analyze
            doc_id: Document identifier
            
        Returns:
            Tuple of (issues, coverage) lists
        """
        logger.info(f"Starting GDPR Article 28(3) analysis for document: {doc_id}")
        
        issues = []
        coverage = []
        
        # Normalize text for analysis
        normalized_text = self._normalize_text(text)
        
        # Analyze each obligation
        for obligation_key, obligation_config in self.obligation_patterns.items():
            logger.debug(f"Analyzing obligation: {obligation_key}")
            
            obligation_issues, obligation_coverage = self._analyze_obligation(
                normalized_text, obligation_key, obligation_config, doc_id
            )
            
            issues.extend(obligation_issues)
            coverage.append(obligation_coverage)
        
        logger.info(f"Analysis complete. Found {len(issues)} issues across {len(coverage)} obligations")
        return issues, coverage
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for consistent pattern matching."""
        # Convert to lowercase
        text = text.lower()
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra punctuation for pattern matching
        text = re.sub(r'[^\w\s\(\)\-\.]', ' ', text)
        
        return text.strip()
    
    def _analyze_obligation(
        self, 
        text: str, 
        obligation_key: str, 
        obligation_config: Dict, 
        doc_id: str
    ) -> Tuple[List[Issue], Coverage]:
        """Analyze a specific GDPR Article 28(3) obligation."""
        
        strong_patterns = obligation_config["strong_patterns"]
        weak_patterns = obligation_config["weak_patterns"]
        obligation_name = obligation_config["name"]
        
        issues = []
        
        # Check for strong implementations
        strong_matches = []
        for pattern in strong_patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            strong_matches.extend(matches)
        
        # Check for weak implementations
        weak_matches = []
        for pattern in weak_patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            weak_matches.extend(matches)
        
        # Check for general weak language in context
        weak_language_found = self._check_weak_language_in_context(text, obligation_key)
        
        # Determine coverage status
        if strong_matches:
            if weak_language_found:
                # Strong pattern but with weak language nearby
                status = CoverageStatusEnum.PARTIAL
                strength = "medium"
                confidence = 0.75
                
                # Create issue for weak language
                issue = self._create_weak_language_issue(
                    doc_id, obligation_key, obligation_name, weak_language_found, text
                )
                issues.append(issue)
                
            else:
                # Strong implementation
                status = CoverageStatusEnum.OK
                strength = "strong"
                confidence = 0.90
                
        elif weak_matches:
            # Only weak implementation found
            status = CoverageStatusEnum.PARTIAL
            strength = "weak"
            confidence = 0.70
            
            # Create issue for weak implementation
            issue = self._create_weak_implementation_issue(
                doc_id, obligation_key, obligation_name, weak_matches[0], text
            )
            issues.append(issue)
            
        else:
            # No implementation found
            status = CoverageStatusEnum.GAP
            strength = "absent"
            confidence = 0.85
            
            # Create issue for missing obligation
            issue = self._create_missing_obligation_issue(
                doc_id, obligation_key, obligation_name
            )
            issues.append(issue)
        
        # Create coverage assessment
        coverage = create_coverage(
            article=obligation_key.replace("_", "(") + ")",
            status=status,
            confidence=confidence,
            present=status != CoverageStatusEnum.GAP,
            strength=strength
        )
        
        return issues, coverage
    
    def _check_weak_language_in_context(self, text: str, obligation_key: str) -> Optional[str]:
        """Check for weak language patterns in the context of an obligation."""
        for pattern in self.weak_language_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def _create_weak_language_issue(
        self, 
        doc_id: str, 
        obligation_key: str, 
        obligation_name: str, 
        weak_phrase: str, 
        text: str
    ) -> Issue:
        """Create an issue for weak language in obligation implementation."""
        
        snippet = self._extract_snippet(text, weak_phrase)
        
        return create_issue(
            doc_id=doc_id,
            clause_path=f"gdpr.{obligation_key}",
            citation=f"GDPR Article {obligation_key.replace('_', '(')})",
            severity=SeverityEnum.MEDIUM,
            confidence=0.75,
            snippet=snippet,
            recommendation=f"Replace weak language '{weak_phrase}' with definitive obligations for {obligation_name.lower()}.",
            issue_type=IssueTypeEnum.GDPR
        )
    
    def _create_weak_implementation_issue(
        self, 
        doc_id: str, 
        obligation_key: str, 
        obligation_name: str, 
        match: re.Match, 
        text: str
    ) -> Issue:
        """Create an issue for weak implementation of obligation."""
        
        snippet = self._extract_snippet(text, match.group(0))
        
        return create_issue(
            doc_id=doc_id,
            clause_path=f"gdpr.{obligation_key}",
            citation=f"GDPR Article {obligation_key.replace('_', '(')})",
            severity=SeverityEnum.HIGH,
            confidence=0.80,
            snippet=snippet,
            recommendation=f"Strengthen {obligation_name.lower()} clause with more specific and binding obligations.",
            issue_type=IssueTypeEnum.GDPR
        )
    
    def _create_missing_obligation_issue(
        self, 
        doc_id: str, 
        obligation_key: str, 
        obligation_name: str
    ) -> Issue:
        """Create an issue for missing obligation."""
        
        return create_issue(
            doc_id=doc_id,
            clause_path=f"gdpr.{obligation_key}",
            citation=f"GDPR Article {obligation_key.replace('_', '(')})",
            severity=SeverityEnum.HIGH,
            confidence=0.90,
            snippet="No relevant clause found",
            recommendation=f"Add clause addressing {obligation_name.lower()} as required by GDPR Article 28(3).",
            issue_type=IssueTypeEnum.GDPR
        )
    
    def _extract_snippet(self, text: str, target_phrase: str, context_length: int = 150) -> str:
        """Extract a snippet around the target phrase for context."""
        try:
            # Find the phrase in the text
            match = re.search(re.escape(target_phrase), text, re.IGNORECASE)
            if not match:
                return target_phrase
            
            start = max(0, match.start() - context_length // 2)
            end = min(len(text), match.end() + context_length // 2)
            
            snippet = text[start:end].strip()
            
            # Add ellipsis if truncated
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."
            
            return snippet
            
        except Exception as e:
            logger.warning(f"Failed to extract snippet for '{target_phrase}': {e}")
            return target_phrase


# Service instance
gdpr_analyzer = GDPRArticle28Analyzer()