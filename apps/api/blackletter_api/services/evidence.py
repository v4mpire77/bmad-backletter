from __future__ import annotations

from typing import List, Tuple, Dict, Optional

# Sentence index shape: list of (start, end) char offsets for each sentence in full text
SentenceIndex = List[Tuple[int, int]]


class EvidenceWindow:
    def __init__(self, text: str, start: int, end: int):
        self.text = text
        self.start = start
        self.end = end

    def dict(self):
        return {"text": self.text, "start": self.start, "end": self.end}


def _build_window_new_api(
    *,
    full_text: str,
    sentences: SentenceIndex,
    span_start: int,
    span_end: int,
    detector_id: Optional[str] = None,
    default_window: int = 2,
    per_detector_windows: Optional[Dict[str, int]] = None,
) -> EvidenceWindow:
    """
    Compute an evidence window around (span_start, span_end) limited to ±N sentences.

    - `sentences` is a list of (start, end) pairs for each sentence in the document.
    - `default_window` is the ±N around the sentence that contains the span.
    - `per_detector_windows` can override N for specific detector ids.
    """
    if span_start > span_end:
        span_start, span_end = span_end, span_start

    n = default_window
    if per_detector_windows and detector_id in per_detector_windows:
        try:
            n = int(per_detector_windows[detector_id])
        except Exception:
            n = default_window

    # find the sentence index that overlaps the span (first hit wins)
    pivot_idx: Optional[int] = None
    valid_sentences: List[Tuple[int, int, int]] = []  # (idx, start, end)
    for i, (s, e) in enumerate(sentences or []):
        if s is None or e is None:
            continue
        valid_sentences.append((i, s, e))
        if s <= span_end and e >= span_start:  # overlap
            pivot_idx = i
            break
    if pivot_idx is None:
        # If we have a valid sentence map but no overlap, choose the nearest sentence
        if valid_sentences:
            first_idx, first_start, _ = valid_sentences[0]
            last_idx, _, last_end = valid_sentences[-1]
            if span_start < first_start:
                pivot_idx = first_idx
            elif span_start > last_end:
                pivot_idx = last_idx
            else:
                # Between sentences: choose the sentence whose boundary is closest to span_start
                # Start with the last sentence whose end <= span_start
                candidate_idx = first_idx
                candidate_end = valid_sentences[0][2]
                for i, s, e in valid_sentences:
                    if e <= span_start:
                        candidate_idx = i
                        candidate_end = e
                    else:
                        # Compare distance to previous end vs next start
                        if (s - span_start) < (span_start - candidate_end):
                            candidate_idx = i
                        break
                pivot_idx = candidate_idx
        else:
            # Fallback: no sentence map at all → clamp to span ± 200 chars
            left = max(0, span_start - 200)
            right = min(len(full_text), span_end + 200)
            return EvidenceWindow(full_text[left:right], left, right)

    lo = max(0, pivot_idx - n)
    hi = min(len(sentences) - 1, pivot_idx + n)

    # Compose window bounds from sentence map
    try:
        win_start = min(s for (s, _) in sentences[lo : hi + 1] if s is not None)
        win_end = max(e for (_, e) in sentences[lo : hi + 1] if e is not None)
    except ValueError:
        # All were None? Fallback to span
        win_start, win_end = span_start, span_end

    # Clamp and slice
    win_start = max(0, min(win_start, len(full_text)))
    win_end = max(win_start, min(win_end, len(full_text)))

    return EvidenceWindow(full_text[win_start:win_end], win_start, win_end)


# Legacy compatibility functions for existing code
def build_configurable_window(
    sentences: List[Dict],
    target_page: int,
    target_span: Tuple[int, int],
    detector_config: Optional[Dict] = None,
    default_window_size: int = 2,
) -> Dict:
    """Compatibility function that applies detector-specific window config and delegates to legacy build_window."""
    # Resolve before/after from detector config or defaults
    before = default_window_size
    after = default_window_size
    if detector_config:
        window_cfg = detector_config.get("window", {}) or {}
        before = window_cfg.get("before", before)
        after = window_cfg.get("after", after)
    # Hard cap to prevent runaway windows
    before = min(int(before), 10)
    after = min(int(after), 10)

    return build_window(
        sentences,
        target_page=target_page,
        target_span=target_span,
        before=before,
        after=after,
    )


def _build_window_legacy(
    sentences: List[Dict],
    *,
    target_page: int,
    target_span: Tuple[int, int],
    before: int = 2,
    after: int = 2,
) -> Dict:
    """
    Legacy/test-oriented evidence window constructor expected by unit tests.

    - Filters sentences by page
    - Selects the target sentence containing span_start; if none, chooses nearest on the page
    - Builds a window limited to [before, after] sentences without crossing page boundaries
    - Returns a dict with page, start/end offsets, concatenated text, indices and window_size
    """
    # Normalize/cap window sizes
    before_capped = min(int(before), 10)
    after_capped = min(int(after), 10)

    # Filter and order sentences for the page
    page_sentences: List[Dict] = [s for s in sentences if s.get("page") == target_page]
    page_sentences.sort(key=lambda x: x.get("start", 0))

    if not page_sentences:
        return {
            "page": target_page,
            "start": 0,
            "end": 0,
            "text": "",
            "sentence_indices": [],
            "target_sentence_idx": 0,
            "window_size": {"before": before_capped, "after": after_capped},
        }

    span_start, span_end = target_span

    # Locate target sentence index (prefer containment of span_start)
    target_idx: Optional[int] = None
    for i, s in enumerate(page_sentences):
        s_start = s.get("start", 0)
        s_end = s.get("end", 0)
        if s_start <= span_start <= s_end:
            target_idx = i
            break

    if target_idx is None:
        # Choose nearest by position on page
        first_start = page_sentences[0].get("start", 0)
        last_end = page_sentences[-1].get("end", 0)
        if span_start < first_start:
            target_idx = 0
        elif span_start > last_end:
            target_idx = len(page_sentences) - 1
        else:
            # Between sentences: pick the one whose boundary is closest to span_start
            # This simplifies to the last sentence whose end <= span_start
            target_idx = 0
            for i, s in enumerate(page_sentences):
                if s.get("end", 0) <= span_start:
                    target_idx = i

    lo = max(0, target_idx - before_capped)
    hi = min(len(page_sentences) - 1, target_idx + after_capped)
    idxs = list(range(lo, hi + 1))

    text_parts = [(page_sentences[i].get("text") or "").strip() for i in idxs]
    text = " ".join([t for t in text_parts if t]).strip()

    start = page_sentences[lo].get("start", 0)
    end = page_sentences[hi].get("end", start)

    return {
        "page": target_page,
        "start": start,
        "end": end,
        "text": text,
        "sentence_indices": idxs,
        "target_sentence_idx": target_idx,
        "window_size": {"before": before_capped, "after": after_capped},
    }


def build_window(*args, **kwargs):
    """
    Unified API that supports both:
    - Spec API: build_window(full_text=..., sentences=[(start,end),...], span_start=..., span_end=..., detector_id=?, default_window=?, per_detector_windows=?) -> EvidenceWindow
    - Legacy API: build_window(sentences=[{page,start,end,text},...], target_page=..., target_span=(start,end), before=?, after=?) -> dict
    """
    if "full_text" in kwargs:
        # Spec API path
        return _build_window_new_api(
            full_text=kwargs.get("full_text", ""),
            sentences=kwargs.get("sentences") or [],
            span_start=kwargs.get("span_start", 0),
            span_end=kwargs.get("span_end", 0),
            detector_id=kwargs.get("detector_id"),
            default_window=kwargs.get("default_window", 2),
            per_detector_windows=kwargs.get("per_detector_windows"),
        )

    # Legacy API path — allow both positional (sentences) and keyword-only
    if args:
        sentences = args[0]
    else:
        sentences = kwargs.get("sentences", [])
    return _build_window_legacy(
        sentences,
        target_page=kwargs.get("target_page", 1),
        target_span=kwargs.get("target_span", (0, 0)),
        before=kwargs.get("before", 2),
        after=kwargs.get("after", 2),
    )

