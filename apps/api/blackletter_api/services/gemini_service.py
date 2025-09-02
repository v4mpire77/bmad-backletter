from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any, Optional, List, Dict

class _Settings:
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-pro"
    gemini_max_tokens: int = 2048
    gemini_temperature: float = 0.0


settings = _Settings()

import sys
sys.modules.setdefault("blackletter_api.services.gemini_service", sys.modules[__name__])


class GeminiClientProtocol:
    def generate_content(self, *args, **kwargs) -> Any: ...


genai = None  # populated when real client available


@dataclass
class GeminiAnalysisResult:
    summary: str
    key_terms: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    confidence_score: float
    raw_response: Dict[str, Any]


@dataclass
class GeminiChatResponse:
    response: str
    suggestions: List[str]
    follow_up_questions: List[str]


class GeminiService:
    def __init__(self, api_key: Optional[str] = None, client: Optional[GeminiClientProtocol] = None):
        """Dependency-injectable Gemini service"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or getattr(settings, "gemini_api_key", None)
        self.client: Optional[GeminiClientProtocol] = client
        self.model: Optional[GeminiClientProtocol] = None

        if self.client is None and self.api_key:
            try:
                global genai
                if genai is None:
                    import google.generativeai as genai  # type: ignore
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel("gemini-1.5-pro")
            except Exception:
                self.client = None
        self.model = self.client

    def _ensure_client(self):
        if not self.client:
            raise RuntimeError("Gemini client not configured")

    def is_available(self) -> bool:
        return self.client is not None

    def analyze_contract(self, text: str) -> str:
        self._ensure_client()
        resp = self.client.generate_content([{"text": f"Analyze contract:\n{text}"}])  # type: ignore[attr-defined]
        # tests assume a .text payload
        return getattr(resp, "text", str(resp))

    def summarize_contract(self, text: str) -> str:
        self._ensure_client()
        resp = self.client.generate_content([{"text": f"Summarize:\n{text}"}])  # type: ignore[attr-defined]
        return getattr(resp, "text", str(resp))

