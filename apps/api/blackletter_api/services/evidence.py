from __future__ import annotations

from typing import Dict, List, Tuple
import logging

from .storage import get_extraction_metadata

logger = logging.getLogger(__name__)


def build_window(
    analysis_id: str,
    start: int,
    end: int,
    n_sentences: int = 2,
) -> Dict:
    """Build an evidence window around a character span.

    Loads sentence and page metadata produced by Story 1.2 and returns a
    snippet containing ``±n_sentences`` around the span. If metadata cannot be
    loaded, an empty snippet is returned.
    """
    meta = get_extraction_metadata(analysis_id)
    if not meta:
        return {
            "snippet": "",
            "page": 0,
            "start": start,
            "end": end,
            "analysis_id": analysis_id,
            "sentence_window": n_sentences,
        }

    page_map = meta.get("page_map", [])
    sentences = meta.get("sentences", [])

    # Determine pages containing the start and end characters
    start_page = 0
    end_page = 0
    for p in page_map:
        p_start = p.get("start", 0)
        p_end = p.get("end", 0)
        if p_start <= start < p_end:
            start_page = p.get("page", 0)
        if p_start <= end < p_end:
            end_page = p.get("page", 0)

    if not start_page and page_map:
        start_page = page_map[0].get("page", 0)
    if not end_page:
        end_page = start_page

    relevant_pages = range(min(start_page, end_page), max(start_page, end_page) + 1)
    page_sents = [s for s in sentences if s.get("page") in relevant_pages]

    # Find sentence indices covering both start and end
    start_idx = 0
    for i, s in enumerate(page_sents):
        if s["start"] <= start <= s["end"] or start < s["start"]:
            start_idx = i
            break

    end_idx = start_idx
    for j in range(start_idx, len(page_sents)):
        s = page_sents[j]
        if end <= s["end"]:
            end_idx = j
            break
    else:
        end_idx = len(page_sents) - 1

    window_start_idx = max(0, start_idx - n_sentences)
    window_end_idx = min(len(page_sents), end_idx + n_sentences + 1)
    selected = page_sents[window_start_idx:window_end_idx]

    if not selected:
        return {
            "snippet": "",
            "page": start_page,
            "start": start,
            "end": end,
            "analysis_id": analysis_id,
            "sentence_window": n_sentences,
        }

    window_start = selected[0]["start"]
    window_end = selected[-1]["end"]
    snippet = " ".join(s["text"] for s in selected)

    return {
        "snippet": snippet,
        "page": start_page,
        "start": window_start,
        "end": window_end,
        "analysis_id": analysis_id,
        "sentence_window": n_sentences,
    }


def build_window_legacy(
    sentences: List[Dict],
    target_page: int,
    target_span: Tuple[int, int],
    before: int = 2,
    after: int = 2,
) -> Dict:
    """Legacy implementation - kept for backward compatibility."""
    start_char, end_char = target_span
    page_sents = [s for s in sentences if s.get("page") == target_page]
    # find the sentence index covering or nearest preceding the target span
    idx = 0
    for i, s in enumerate(page_sents):
        if s["start"] <= start_char <= s["end"] or start_char < s["start"]:
            idx = i
            break
    start_idx = max(0, idx - before)
    end_idx = min(len(page_sents), idx + after + 1)
    selected = page_sents[start_idx:end_idx]
    if not selected:
        return {"page": target_page, "start": 0, "end": 0, "text": "", "sentence_indices": []}
    window_start = selected[0]["start"]
    window_end = selected[-1]["end"]
    text = " ".join(s["text"] for s in selected)
    return {
        "page": target_page,
        "start": window_start,
        "end": window_end,
        "text": text,
        "sentence_indices": list(range(start_idx, end_idx)),
    }


def handle_boundary_cases(
    text: str,
    start: int,
    end: int,
    n_sentences: int = 2
) -> Dict:
    """
    Handle boundary cases for evidence window:
    - Spans inside a sentence
    - Spans across sentences  
    - Near beginning/end of document
    - Non-ASCII characters
    """
    # Basic implementation for boundary case handling
    text_len = len(text)
    
    # Handle start of document
    if start < n_sentences * 50:  # Rough estimate of sentence length
        actual_start = 0
    else:
        actual_start = max(0, start - n_sentences * 50)
    
    # Handle end of document    
    if end > text_len - n_sentences * 50:
        actual_end = text_len
    else:
        actual_end = min(text_len, end + n_sentences * 50)
    
    # Extract snippet ensuring we handle non-ASCII properly
    snippet = text[actual_start:actual_end]
    
    return {
        "snippet": snippet,
        "start": actual_start,
        "end": actual_end,
        "original_start": start,
        "original_end": end,
        "boundary_adjusted": actual_start != start or actual_end != end
    }

