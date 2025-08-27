from __future__ import annotations

from typing import Dict, List, Tuple


def build_window(
    sentences: List[Dict],
    target_page: int,
    target_span: Tuple[int, int],
    before: int = 2,
    after: int = 2,
) -> Dict:
    """Given per-page sentence index entries and a target span on a page,
    return a window of up to `before` + `after` sentences around the span.
    Avoid crossing page boundaries.
    """
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

