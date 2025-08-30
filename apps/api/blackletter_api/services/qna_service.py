from __future__ import annotations

from difflib import SequenceMatcher
from typing import Dict, List

DOCUMENT_STORE: Dict[str, List[str]] = {}


def add_document(document_id: str, text: str) -> None:
    """Register a document's text in the in-memory store."""
    chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]
    DOCUMENT_STORE[document_id] = chunks


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def get_relevant_chunks(document_id: str, question: str, top_k: int = 3) -> List[str]:
    """Return the top_k chunks most similar to the question."""
    chunks = DOCUMENT_STORE.get(document_id, [])
    scored = sorted(chunks, key=lambda c: _similarity(question, c), reverse=True)
    return scored[:top_k]


def answer_question(document_id: str, question: str) -> str:
    """Return the most relevant chunk for the given question."""
    chunks = get_relevant_chunks(document_id, question, top_k=1)
    return chunks[0] if chunks else ""

