"""
LLM Service module providing a unified interface for contract analysis.

This module wraps the existing LLMAdapter to provide a consistent interface
for testing and use throughout the application.
"""


import asyncio
from dataclasses import dataclass
from typing import Any, Dict
from backend.app.core.llm_adapter import LLMAdapter


class LLMService:
    """
    Service class for LLM operations, particularly contract analysis.
    
    This class provides a simple interface to interact with various LLM providers
    (Gemini, Ollama) through the underlying LLMAdapter.
    """
    
    def __init__(self):
        """Initialize the LLM service with the configured adapter."""
        try:
            self.adapter = LLMAdapter()
        except RuntimeError as exc:
            # Fall back to a stub adapter so the service remains usable in tests
            self.adapter = _StubAdapter(str(exc))
        self.provider = self.adapter.provider

        if self.adapter.init_error:
            print(f"⚠️  Warning: {self.adapter.init_error}")
    
    async def analyze_contract(self, contract_text: str) -> dict:
        """
        Analyze a contract and return structured results.
        
        Args:
            contract_text (str): The contract text to analyze
            
        Returns:
            dict: Analysis results with keys like 'summary', 'risks', 'dates', etc.
        """
        return await self.adapter.analyze_contract(contract_text)
    
    def get_provider_info(self) -> dict:
        """
        Get information about the current LLM provider configuration.
        
        Returns:
            dict: Provider information including name, model, and status
        """
        return {
            "provider": self.adapter.provider,
            "model": self.adapter.model,
            "gemini_configured": bool(self.adapter.gemini_key),
            "ollama_available": self.adapter.ollama_reachable,
            "init_error": self.adapter.init_error
        }


@dataclass
class _StubAdapter:
    """Simple stand-in used when no real provider is configured."""

    init_error: str
    provider: str = "stub"
    model: str = "stub"
    gemini_key: Any = None
    ollama_reachable: bool = False

    async def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        summary = (contract_text[:400] + "…") if len(contract_text) > 400 else contract_text
        return {"summary": summary, "risks": [], "dates": [], "error": self.init_error}
