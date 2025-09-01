"""Utilities for exporting retrieval results."""

from __future__ import annotations

import csv
from io import StringIO
from typing import Dict, Iterable, List


def results_to_csv(results: Iterable[Dict]) -> str:
    """Return a CSV representation of retrieval ``results``.

    Parameters
    ----------
    results:
        An iterable of dictionaries representing retrieval output.  If the
        iterable is empty an empty string is returned.
    """

    results = list(results)
    if not results:
        return ""

    fieldnames = list(results[0].keys())
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)
    return buf.getvalue()


__all__ = ["results_to_csv"]
