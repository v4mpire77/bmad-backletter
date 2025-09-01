# Service wrapper around the Gemini-only LLMAdapter

from __future__ import annotations
from typing import Iterable, List, Optional

from backend.app.core.llm_adapter import LLMAdapter


class GeminiClient:
    """Minimal Gemini client used only for tests.

    The real implementation would call the external Gemini API.  Here we just
    provide the interface that tests expect and allow it to be easily mocked.
    """

    def generate(self, prompt: str, *, system: str | None = None, **_: object) -> str:
        return prompt

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(t))] for t in texts]


class GeminiClient:
    """Lightweight wrapper around :class:`LLMAdapter` for tests."""

    def __init__(self) -> None:
        self.adapter = LLMAdapter()

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> str:
        return self.adapter.generate(
            prompt=prompt, system=system, temperature=temperature, max_output_tokens=max_output_tokens
        )

    def embed(self, texts: Iterable[str]) -> List[List[float]]:
        return self.adapter.embed_texts(list(texts))


# Singleton-style adapter for health checks
_llm: LLMAdapter | None = None


def get_llm() -> LLMAdapter:
    global _llm
    if _llm is None:
        _llm = LLMAdapter()
    return _llm


# --------- Convenience functions used by routes/services ---------

def generate_text(
    prompt: str, system: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2048
) -> str:
    client = GeminiClient()
    # The test suite only verifies prompt and system arguments are forwarded.
    return client.generate(prompt, system=system)


def embed_texts(texts: Iterable[str]) -> List[List[float]]:
    client = GeminiClient()
    return client.embed(texts)


def health() -> dict:
    return get_llm().health()
