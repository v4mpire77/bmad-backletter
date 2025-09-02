"""
Gemini Judge Service

LLM-powered contract analysis using Google's Gemini model.
"""
import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List

import httpx

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
        """Analyze contract snippet against GDPR rule."""

        prompt = self._build_analysis_prompt(rule, snippet, context, citations)

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(url, json=payload)
                    response.raise_for_status()

                model_resp = response.json()
                text = model_resp["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(text)

                return JudgmentResult(
                    rule_id=rule["id"],
                    verdict=data.get("verdict", "insufficient_context"),
                    risk=data.get("risk", "low"),
                    rationale=data.get("rationale", ""),
                    improvements=data.get("improvements", []),
                    quotes=data.get("quotes", []),
                    confidence=float(data.get("confidence", 0.0)),
                )
            except (
                httpx.TimeoutException,
                httpx.RequestError,
                httpx.HTTPStatusError,
                KeyError,
                json.JSONDecodeError,
            ) as exc:
                if attempt == 2:
                    raise RuntimeError("Gemini API request failed") from exc
                await asyncio.sleep(2 ** attempt)
    
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
