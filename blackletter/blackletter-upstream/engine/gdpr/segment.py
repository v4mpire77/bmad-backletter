"""Utilities for segmenting contract text into clauses."""

import re
from typing import Dict, List, Optional


def segment_clauses(text: str) -> List[Dict[str, Optional[str]]]:
    """Split contract text into clauses based on heading patterns.

    Returns a list of dictionaries each containing ``id`` and ``text`` keys.
    If no headings are detected the entire text becomes a single clause with
    ``id`` set to ``None``.
    """

    pattern = re.compile(
        r"^(?P<cid>(?:(?:Section|Article|Clause)\s+)?\d+(?:\.\d+)*\.?)",
        flags=re.IGNORECASE | re.MULTILINE,
    )

    matches = list(pattern.finditer(text))
    if not matches:
        return [{"id": None, "text": text.strip()}]

    clauses: List[Dict[str, Optional[str]]] = []
    for idx, match in enumerate(matches):
        cid = match.group("cid").rstrip(".")
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        clauses.append({"id": cid, "text": text[start:end].strip()})

    return clauses
