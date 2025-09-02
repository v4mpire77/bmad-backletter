from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import json
import logging

from .storage import analysis_dir

logger = logging.getLogger(__name__)


def build_window(
    analysis_id: str,
    start: int,
    end: int,
    n_sentences: int = 2,
) -> Dict:
    """Build an evidence window around a finding span.

    This implementation loads sentence and page metadata from
    ``analysis_dir/<analysis_id>/sentences.json`` produced in Story 1.2.

    Args:
        analysis_id: The analysis ID of the document being inspected.
        start: Global start character position of the finding.
        end: Global end character position of the finding.
        n_sentences: Number of sentences before/after the finding.

    Returns:
        Dict with: { snippet, page, start, end } where start/end are global
        offsets in the concatenated document text.
    """
    data_path = analysis_dir(analysis_id) / "sentences.json"
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except Exception:
        logger.warning("sentences.json missing for analysis %s", analysis_id)
        return {"snippet": "", "page": 0, "start": start, "end": end}

    sentences: List[Dict] = data.get("sentences", [])
    page_map: List[Dict] = data.get("page_map", [])

    # Find the page containing the start offset
    page_info: Optional[Dict] = next(
        (p for p in page_map if p.get("start") <= start < p.get("end")), None
    )
    if not page_info:
        return {"snippet": "", "page": 0, "start": start, "end": end}

    page_num = int(page_info["page"])
    page_start = int(page_info["start"])

    # Sentences are stored with offsets relative to their page
    local_start = start - page_start
    page_sentences = [s for s in sentences if s.get("page") == page_num]

    # Determine the sentence index covering the span start
    idx = len(page_sentences) - 1
    for i, s in enumerate(page_sentences):
        s_start = int(s.get("start", 0))
        s_end = int(s.get("end", 0))
        if s_start <= local_start < s_end or local_start < s_start:
            idx = i
            break

    start_idx = max(0, idx - n_sentences)
    end_idx = min(len(page_sentences), idx + n_sentences + 1)
    selected = page_sentences[start_idx:end_idx]
    if not selected:
        return {"snippet": "", "page": page_num, "start": start, "end": start}

    snippet = " ".join(s["text"] for s in selected)
    window_start = page_start + int(selected[0]["start"])
    window_end = page_start + int(selected[-1]["end"])

    return {"snippet": snippet, "page": page_num, "start": window_start, "end": window_end}


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

