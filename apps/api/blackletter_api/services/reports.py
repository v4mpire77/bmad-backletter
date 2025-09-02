from __future__ import annotations

"""Utilities for generating analysis reports as PDF files."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, select_autoescape
from xhtml2pdf import pisa

TEMPLATE = """\
<html>
  <body>
    <h1>Report for {{ analysis.filename }}</h1>
    <p>Analysis ID: {{ analysis.id }}</p>
  </body>
</html>
"""

env = Environment(autoescape=select_autoescape())


def render_report_html(analysis: Any) -> str:
    """Render an HTML report for an analysis object."""
    template = env.from_string(TEMPLATE)
    return template.render(analysis=analysis)


def html_to_pdf(html: str, output_path: Path) -> Path:
    """Convert HTML content into a PDF file at the given path."""
    with open(output_path, "wb") as f:
        result = pisa.CreatePDF(html, dest=f)
    if result.err:
        raise RuntimeError("PDF generation failed")
    return output_path


def generate_report_pdf(analysis: Any, output_path: Path) -> Path:
    """Generate a PDF report for the given analysis and return the path."""
    html = render_report_html(analysis)
    return html_to_pdf(html, output_path)
