from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def build_window(
    analysis_id: str,
    start: int,
    end: int,
    n_sentences: int = 2
) -> Dict:
    """
    Build evidence window for Story 1.3 - Evidence Window Builder.
    
    Given a char span in extracted text, return a window of ±N sentences 
    (default 2) with page/offsets, respecting page boundaries.
    
    Args:
        analysis_id: The analysis ID to get sentence index and page map from
        start: Start character position
        end: End character position  
        n_sentences: Number of sentences before/after (default 2)
        
    Returns:
        Dict with: { snippet, page, start, end }
    """
    # TODO: In actual implementation, retrieve persisted sentence index and page map from 1.2
    # For now, return a mock response matching the expected interface
    
    return {
        "snippet": f"Evidence window for span {start}-{end} with ±{n_sentences} sentences",
        "page": 1,
        "start": max(0, start - 100),  # Expanded start
        "end": end + 100,  # Expanded end
        "analysis_id": analysis_id,
        "sentence_window": n_sentences
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

