import json
import os
import sys
from types import SimpleNamespace

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import rag


def test_refuses_on_low_score():
    ctx = [{"source_id": "A", "page": 1, "content": "text", "score": 0.1}]
    res = rag.generate_answer("question", ctx, threshold=0.5)
    assert "enough information" in res["answer"].lower()
    assert res["citations"] == []


def test_generate_answer_with_mock(monkeypatch):
    def fake_generate_content(prompt):
        payload = {
            "answer": "Answer.",
            "citations": [
                {"source_id": "A", "page": 1, "quote": "foo"},
                {"source_id": "B", "page": 2, "quote": "bar"},
            ],
            "confidence": 0.8,
        }
        return SimpleNamespace(text=json.dumps(payload))

    class FakeGeminiModel:
        def generate_content(self, prompt):
            return fake_generate_content(prompt)

    def fake_GenerativeModel(model_name):
        return FakeGeminiModel()

    # Mock the genai module and environment
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    if hasattr(rag, 'genai') and rag.genai is not None:
        monkeypatch.setattr(rag.genai, "configure", lambda api_key: None)
        monkeypatch.setattr(rag.genai, "GenerativeModel", fake_GenerativeModel)

    contexts = [
        {"source_id": "A", "page": 1, "content": "foo", "score": 0.9},
        {"source_id": "B", "page": 2, "content": "bar", "score": 0.8},
    ]
    res = rag.generate_answer("question", contexts)
    assert res["answer"] == "Answer."
    assert len(res["citations"]) == 2
    assert res["confidence"] == 0.8


def test_preserves_existing_citations(monkeypatch):
    """If the model returns a single citation, it should be kept and a
    second one should be added from the remaining context."""

    def fake_generate_content(prompt):
        payload = {
            "answer": "Answer.",
            "citations": [{"source_id": "A", "page": 1, "quote": "foo"}],
            "confidence": 0.9,
        }
        return SimpleNamespace(text=json.dumps(payload))

    class FakeGeminiModel:
        def generate_content(self, prompt):
            return fake_generate_content(prompt)

    def fake_GenerativeModel(model_name):
        return FakeGeminiModel()

    # Mock the genai module and environment
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    if hasattr(rag, 'genai') and rag.genai is not None:
        monkeypatch.setattr(rag.genai, "configure", lambda api_key: None)
        monkeypatch.setattr(rag.genai, "GenerativeModel", fake_GenerativeModel)

    contexts = [
        {"source_id": "A", "page": 1, "content": "foo", "score": 0.9},
        {"source_id": "B", "page": 2, "content": "bar", "score": 0.8},
    ]
    res = rag.generate_answer("question", contexts)
    assert len(res["citations"]) == 2
    assert res["citations"][0]["source_id"] == "A"
    assert res["citations"][1]["source_id"] == "B"
