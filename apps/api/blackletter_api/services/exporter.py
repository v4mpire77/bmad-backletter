from __future__ import annotations

from pathlib import Path
from typing import Iterable

from ..models.schemas import Finding
from .storage import analysis_dir


def generate_html_export(analysis_id: str, findings: Iterable[Finding]) -> Path:
    """Render a minimal HTML report summarizing findings."""
    a_dir = analysis_dir(analysis_id)
    out_path = a_dir / "report.html"
    html_parts = ["<html><body><h1>Findings</h1>", "<ul>"]
    for f in findings:
        html_parts.append(
            f"<li>Detector {f.detector_id} on page {f.page}: {f.snippet}</li>"
        )
    html_parts.append("</ul></body></html>")
    out_path.write_text("".join(html_parts), encoding="utf-8")
    return out_path
