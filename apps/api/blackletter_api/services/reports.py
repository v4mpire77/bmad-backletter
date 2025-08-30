from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .storage import analysis_dir
from ..models.schemas import ExportOptions, ReportExport


def _load_artifacts(base: Path) -> Dict[str, Any]:
    import json

    analysis = {}
    findings = []
    a = base / "analysis.json"
    f = base / "findings.json"
    try:
        if a.exists():
            analysis = json.loads(a.read_text(encoding="utf-8"))
    except Exception:
        analysis = {}
    try:
        if f.exists():
            findings = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        findings = []
    return {"analysis": analysis, "findings": findings}


def _jinja_env(templates_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def generate_report(analysis_id: str, options: ExportOptions) -> ReportExport:
    """Render a deterministic HTML report from stored artifacts and persist it.

    Returns a ReportExport record containing metadata and filename.
    """
    base = analysis_dir(analysis_id)
    artifacts = _load_artifacts(base)

    # Prepare template environment
    templates_dir = Path(__file__).resolve().parents[1] / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    template_path = templates_dir / "report.html"
    if not template_path.exists():
        # Write a minimal default template if missing
        template_path.write_text(
            """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Blackletter Report</title>
    <style>
      body{ font-family: system-ui, Segoe UI, Arial; margin: 2rem; }
      h1{ margin-bottom: .25rem; }
      .meta{ color:#666; font-size:.9rem; margin-bottom:1rem; }
      .finding{ border-top:1px solid #eee; padding:.5rem 0; }
      .chip{ display:inline-block; padding:.1rem .5rem; border-radius:.5rem; background:#eef; margin-left:.5rem; }
      .muted{ color:#777; }
    </style>
  </head>
  <body>
    <h1>Report for {{ analysis.filename or analysis.id or analysis_id }}</h1>
    <div class="meta">
      Generated: {{ generated_at }} | Format: {{ options.date_format }}
      {% if options.include_meta %}<br/>
        Analysis ID: {{ analysis.id or analysis_id }} | Findings: {{ findings|length }}
      {% endif %}
    </div>

    {% for f in findings %}
      <div class="finding">
        <div>
          <strong>{{ f.rule_id }}</strong>
          <span class="chip">{{ f.verdict }}</span>
        </div>
        <div class="muted">p{{ f.page }} · {{ f.start }}–{{ f.end }}</div>
        <div>{{ f.snippet }}</div>
        <div class="muted">{{ f.rationale }}</div>
      </div>
    {% endfor %}
  </body>
 </html>
            """.strip(),
            encoding="utf-8",
        )

    env = _jinja_env(templates_dir)
    template = env.get_template("report.html")

    # Compose render context
    generated_at = datetime.now(timezone.utc).isoformat()
    ctx = {
        "analysis_id": analysis_id,
        "analysis": artifacts.get("analysis", {}),
        "findings": artifacts.get("findings", []),
        "options": options.model_dump(),
        "generated_at": generated_at,
    }

    html = template.render(**ctx)

    # Persist under reports/
    reports_dir = base / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{analysis_id.upper()}.html"
    out = reports_dir / filename
    out.write_text(html, encoding="utf-8")

    return ReportExport(
        id=str(uuid4()),
        analysis_id=analysis_id,
        filename=filename,
        created_at=generated_at,
        options=options,
    )

