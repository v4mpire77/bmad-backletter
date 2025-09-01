"""
Vague Terms Detector Service

Detects ambiguous language in contracts using regex patterns.
"""
import re
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path

class VagueTermsDetector:
    def __init__(self, rules_path: Optional[str] = None):
        """Initialize with vague terms lexicon."""
        if rules_path is None:
            rules_path = Path(__file__).parent.parent.parent / "rules" / "vague_terms.json"
        
        self.vague_patterns = self._load_vague_terms(rules_path)
    
    def _load_vague_terms(self, path: str) -> Dict[str, List[str]]:
        """Load vague terms patterns from JSON."""
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return data.get('patterns', {})
        except FileNotFoundError:
            # Fallback patterns if file doesn't exist
            return {
                "temporal_vague": [
                    r"as soon as (?:reasonably )?practicable",
                    r"within a reasonable time",
                    r"promptly",
                    r"in due course"
                ],
                "effort_vague": [
                    r"reasonable efforts?",
                    r"best efforts?",
                    r"commercially reasonable",
                    r"good faith efforts?"
                ],
                "scope_vague": [
                    r"to the extent (?:reasonably )?(?:possible|practicable)",
                    r"where appropriate",
                    r"if applicable",
                    r"as may be required"
                ]
            }
    
    def detect_vague_terms(self, text: str, context_window: int = 200) -> List[Dict[str, any]]:
        """
        Detect vague terms in contract text.
        
        Args:
            text: Contract text to analyze
            context_window: Characters before/after match for context
            
        Returns:
            List of vague term findings with context and positions
        """
        findings = []
        
        for category, patterns in self.vague_patterns.items():
            for pattern in patterns:
                try:
                    for match in re.finditer(pattern, text, re.IGNORECASE):
                        start, end = match.span()
                        
                        # Extract context
                        context_start = max(0, start - context_window)
                        context_end = min(len(text), end + context_window)
                        context = text[context_start:context_end]
                        
                        findings.append({
                            "category": category,
                            "pattern": pattern,
                            "matched_text": match.group(),
                            "start_pos": start,
                            "end_pos": end,
                            "context": context,
                            "severity": self._get_severity(category),
                            "suggestion": self._get_suggestion(category, match.group())
                        })
                except re.error as e:
                    print(f"Invalid regex pattern {pattern}: {e}")
                    continue
        
        return findings
    
    def _get_severity(self, category: str) -> str:
        """Map vague term categories to severity levels."""
        severity_map = {
            "temporal_vague": "medium",
            "effort_vague": "high", 
            "scope_vague": "medium"
        }
        return severity_map.get(category, "low")
    
    def _get_suggestion(self, category: str, matched_text: str) -> str:
        """Provide improvement suggestions for vague terms."""
        suggestions = {
            "temporal_vague": f"Replace '{matched_text}' with specific timeframe (e.g., 'within 30 days')",
            "effort_vague": f"Replace '{matched_text}' with measurable obligations",
            "scope_vague": f"Replace '{matched_text}' with specific conditions or criteria"
        }
        return suggestions.get(category, f"Consider making '{matched_text}' more specific")