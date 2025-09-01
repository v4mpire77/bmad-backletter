import json
import os
from typing import Any, Dict, List

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover - gemini may not be installed
    genai = None  # type: ignore

from .prompts import ANSWER_WITH_CITATIONS


def generate_answer(
    query: str,
    contexts: List[Dict[str, Any]],
    *,
    model: str | None = None,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """Generate an answer with citations from retrieved contexts.

    Parameters
    ----------
    query: str
        The question to answer.
    contexts: List[Dict]
        Each context dict should have keys: ``source_id``, ``page``, ``content`` and
        optionally ``score``.
    model: str
        The Gemini model to use (``gemini-2.0-flash`` by default).
    threshold: float
        Minimum retrieval score required to attempt an answer. If all contexts
        fall below this score, the function refuses to answer.
    """

    model = model or os.getenv("RAG_MODEL", "gemini-2.0-flash")

    best_score = max((c.get("score", 0.0) for c in contexts), default=0.0)
    if best_score < threshold or not contexts:
        return {
            "answer": "I don't have enough information to answer that.",
            "citations": [],
            "confidence": 0.0,
        }

    context_lines = [
        f"[{c['source_id']}:{c['page']}] {c['content']}" for c in contexts
    ]
    prompt = ANSWER_WITH_CITATIONS.format(
        question=query, context="\n".join(context_lines)
    )

    if genai is None:  # pragma: no cover - runtime safeguard
        raise RuntimeError("google-generativeai package not available")

    # Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is required")
    
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    
    # Generate response using Gemini
    response = gemini_model.generate_content(prompt)
    text: str = ""
    try:
        text = response.text or ""
    except Exception:  # pragma: no cover - fallback parsing
        text = str(response)

    try:
        data = json.loads(text)
    except Exception:
        data = {
            "answer": text,
            "citations": [],
            "confidence": 0.0,
        }

    # Enforce at least two citations when possible while preserving any
    # citations returned by the model. We append missing citations from the
    # available contexts without duplicating sources that are already cited.
    citations = data.get("citations", [])
    if len(citations) < 2:
        seen = {
            (c.get("source_id"), c.get("page"))
            for c in citations
            if c.get("source_id") is not None and c.get("page") is not None
        }
        for c in contexts:
            key = (c["source_id"], c["page"])
            if key not in seen:
                citations.append(
                    {
                        "source_id": c["source_id"],
                        "page": c["page"],
                        "quote": c["content"][:200],
                    }
                )
                seen.add(key)
            if len(citations) >= 2:
                break
        data["citations"] = citations

    data.setdefault("confidence", float(best_score))
    return data

__all__ = ["generate_answer"]
