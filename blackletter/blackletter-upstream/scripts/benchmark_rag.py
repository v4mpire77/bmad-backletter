"""Simple performance benchmark for RAG answer generation."""
import json
import os
import sys
import time
from types import SimpleNamespace

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import rag


def _mock_genai():
    """Patch rag.genai with a lightweight fake model."""
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
        rag.genai.configure = lambda api_key: None  # type: ignore
        rag.genai.GenerativeModel = fake_GenerativeModel  # type: ignore


def benchmark(iterations: int = 10) -> float:
    """Run the benchmark and return average runtime."""
    _mock_genai()
    ctx = [{"source_id": "A", "page": 1, "content": "text", "score": 0.9}]
    start = time.perf_counter()
    for _ in range(iterations):
        rag.generate_answer("question", ctx)
    end = time.perf_counter()
    avg = (end - start) / iterations
    print(f"Average execution time over {iterations} runs: {avg:.4f}s")
    return avg


if __name__ == "__main__":
    benchmark()
