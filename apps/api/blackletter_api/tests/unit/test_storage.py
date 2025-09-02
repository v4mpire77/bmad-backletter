from __future__ import annotations

import json
from pathlib import Path

from blackletter_api.services import storage


def test_get_analysis_text_reads_file(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "data"
    monkeypatch.setattr(storage, "DATA_ROOT", base)
    analysis_id = "a1"
    analysis_path = storage.analysis_dir(analysis_id)
    (analysis_path / "text.txt").write_text("hello", encoding="utf-8")

    assert storage.get_analysis_text(analysis_id) == "hello"


def test_get_analysis_text_missing_file(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "data"
    monkeypatch.setattr(storage, "DATA_ROOT", base)

    assert storage.get_analysis_text("missing") == ""


def test_get_analysis_findings_reads_json(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "data"
    monkeypatch.setattr(storage, "DATA_ROOT", base)
    analysis_id = "b2"
    analysis_path = storage.analysis_dir(analysis_id)
    findings = [{"id": 1}]
    (analysis_path / "findings.json").write_text(
        json.dumps(findings), encoding="utf-8"
    )

    assert storage.get_analysis_findings(analysis_id) == findings


def test_get_analysis_findings_missing_file(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "data"
    monkeypatch.setattr(storage, "DATA_ROOT", base)

    assert storage.get_analysis_findings("missing") == []

