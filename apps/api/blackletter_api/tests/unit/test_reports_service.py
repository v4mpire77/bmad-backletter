from types import SimpleNamespace

from blackletter_api.services.reports import (
    generate_report_pdf,
    render_report_html,
)


def test_render_report_html_includes_filename():
    analysis = SimpleNamespace(id="123", filename="sample.txt")
    html = render_report_html(analysis)
    assert "sample.txt" in html


def test_generate_report_pdf_creates_file(tmp_path):
    analysis = SimpleNamespace(id="123", filename="sample.txt")
    output = tmp_path / "report.pdf"
    generate_report_pdf(analysis, output)
    assert output.exists()
    assert output.stat().st_size > 0
