import json
import os
import sys
import time
from types import SimpleNamespace

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import rag


def _mock_genai():
    def fake_generate_content(prompt):
        payload = {"answer": "ok", "citations": [], "confidence": 0.9}
        return SimpleNamespace(text=json.dumps(payload))

    class FakeGeminiModel:
        def generate_content(self, prompt):
            return fake_generate_content(prompt)

    def fake_GenerativeModel(_):
        return FakeGeminiModel()

    os.environ.setdefault("GEMINI_API_KEY", "fake-key")
    if hasattr(rag, "genai") and rag.genai is not None:
        rag.genai.configure = lambda api_key: None
        rag.genai.GenerativeModel = fake_GenerativeModel


def test_generate_answer_performance():
    _mock_genai()
    ctx = [{"source_id": "A", "page": 1, "content": "text", "score": 0.9}]
    start = time.perf_counter()
    rag.generate_answer("question", ctx)
    duration = time.perf_counter() - start
    # Ensure mock execution is fast
    assert duration < 0.5
