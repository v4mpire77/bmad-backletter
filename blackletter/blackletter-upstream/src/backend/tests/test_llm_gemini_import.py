# Lightweight tests to validate Gemini-only stack is importable.

def test_google_genai_import():
    import importlib
    mod = importlib.import_module("google.generativeai")
    assert mod is not None


def test_llm_adapter_import_and_health():
    from backend.app.core.llm_adapter import LLMAdapter

    # We don’t require a live API call in CI; just instantiate and check config errors are informative.
    # If GEMINI_API_KEY is not set, LLMAdapter should raise a RuntimeError.
    import os
    key = os.getenv("GEMINI_API_KEY")

    if key:
        llm = LLMAdapter()
        h = llm.health()
        assert h["provider"] == "gemini"
        assert h["ready"] is True
    else:
        import pytest
        with pytest.raises(RuntimeError):
            LLMAdapter()
