"""
Gemini Judge Service

LLM-powered contract analysis using Google's Gemini model.
"""
import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class JudgmentResult:
    """Result from LLM judge analysis."""
    rule_id: str
    verdict: str  # "compliant", "non_compliant", "weak", "insufficient_context"
    risk: str     # "low", "medium", "high"
    rationale: str
    improvements: List[str]
    quotes: List[Dict[str, Any]]
    confidence: float

class GeminiJudge:
    """LLM judge using Gemini for GDPR compliance analysis."""
    
    def __init__(self):
        """Initialize Gemini judge."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
    
    async def judge_rule_compliance(self, 
                                  rule: Dict[str, Any], 
                                  snippet: str, 
                                  context: str,
                                  citations: List[Dict[str, Any]]) -> JudgmentResult:
        """
        Analyze contract snippet against GDPR rule.
        
        Args:
            rule: GDPR rule definition
            snippet: Relevant contract text snippet
            context: Expanded context around snippet
            citations: Citation metadata
            
        Returns:
            JudgmentResult with verdict and analysis
        """
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(rule, snippet, context, citations)
        
        # For now, return a structured mock response
        # TODO: Replace with actual Gemini API call
        return self._mock_gemini_response(rule, snippet)
    
    def _build_analysis_prompt(self, rule: Dict[str, Any], snippet: str, 
                              context: str, citations: List[Dict[str, Any]]) -> str:
        """Build structured prompt for Gemini analysis."""
        
        prompt = f"""You are a GDPR compliance expert analyzing a vendor contract.

RULE TO EVALUATE:
ID: {rule['id']}
Name: {rule['name']}
Article: {rule.get('article', 'N/A')}
Description: {rule['description']}
Severity: {rule['severity']}
Required: {rule['required']}

CONTRACT SNIPPET:
{snippet}

EXPANDED CONTEXT:
{context}

CITATIONS:
{json.dumps(citations, indent=2)}

ANALYSIS REQUIREMENTS:
1. Determine if the contract snippet complies with this GDPR rule
2. Provide a clear verdict: compliant, non_compliant, weak, or insufficient_context
3. Assess risk level: low, medium, high
4. Give detailed rationale with specific quotes from the contract
5. Suggest concrete improvements if non-compliant
6. Include exact quotes with proper citations

RESPONSE FORMAT (JSON):
{{
  "verdict": "compliant|non_compliant|weak|insufficient_context",
  "risk": "low|medium|high", 
  "rationale": "Detailed explanation of your analysis",
  "improvements": ["Specific suggestion 1", "Specific suggestion 2"],
  "quotes": [
    {{
      "text": "exact quote from contract",
      "citation": {{"doc_id": "...", "page": 1, "start": 100, "end": 200}}
    }}
  ],
  "confidence": 0.85
}}

Analyze now:"""
        
        return prompt
    
    def _mock_gemini_response(self, rule: Dict[str, Any], snippet: str) -> JudgmentResult:
        """Generate mock response for testing (replace with real Gemini call)."""
        
        # Simple heuristic analysis for demonstration
        snippet_lower = snippet.lower()
        
        # Check for GDPR-related terms
        gdpr_terms = ["data protection", "personal data", "processing", "consent", "lawful basis"]
        has_gdpr_terms = any(term in snippet_lower for term in gdpr_terms)
        
        # Check for vague language
        vague_terms = ["reasonable", "appropriate", "adequate", "sufficient"]
        has_vague_terms = any(term in snippet_lower for term in vague_terms)
        
        if rule['id'] == 'R01':  # Data processing lawful basis
            if has_gdpr_terms and not has_vague_terms:
                verdict = "compliant"
                risk = "low"
                rationale = "Contract contains clear data processing provisions"
                improvements = []
            elif has_vague_terms:
                verdict = "weak"
                risk = "medium"
                rationale = "Data processing terms present but contain vague language"
                improvements = ["Specify exact lawful basis under GDPR Article 6", "Remove ambiguous terms"]
            else:
                verdict = "non_compliant"
                risk = "high"
                rationale = "No clear lawful basis for data processing identified"
                improvements = ["Add GDPR Article 6 lawful basis clause", "Specify data processing purposes"]
        else:
            # Default analysis for other rules
            verdict = "weak" if has_vague_terms else "compliant"
            risk = "medium" if has_vague_terms else "low"
            rationale = f"Analysis of {rule['name']} - {'vague terms detected' if has_vague_terms else 'appears compliant'}"
            improvements = ["Consider more specific language"] if has_vague_terms else []
        
        return JudgmentResult(
            rule_id=rule['id'],
            verdict=verdict,
            risk=risk,
            rationale=rationale,
            improvements=improvements,
            quotes=[{"text": snippet[:100] + "...", "citation": {"doc_id": "mock", "page": 1, "start": 0, "end": 100}}],
            confidence=0.85
        )
    
    async def batch_analyze(self, analyses: List[Dict[str, Any]]) -> List[JudgmentResult]:
        """Analyze multiple rule/snippet combinations in batch."""
        results = []
        for analysis in analyses:
            result = await self.judge_rule_compliance(
                rule=analysis['rule'],
                snippet=analysis['snippet'],
                context=analysis.get('context', ''),
                citations=analysis.get('citations', [])
            )
            results.append(result)
        return results