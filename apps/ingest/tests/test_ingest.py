from pathlib import Path

from apps.ingest.adapters import ingest_file


def test_ingest_empty_file(tmp_path: Path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")
    chunks = ingest_file(str(file_path), "empty")
    assert chunks == []


def test_ingest_large_file(tmp_path: Path):
    file_path = tmp_path / "large.txt"
    content = "1. Section\n" + ("word " * 1000)
    file_path.write_text(content, encoding="utf-8")
    chunks = ingest_file(str(file_path), "large")
    assert len(chunks) >= 1
    assert chunks[0].tokens >= 1000


def test_ingest_mixed_encodings(tmp_path: Path):
    file_path = tmp_path / "mixed.txt"
    content = "1. Section\nCaf\u00e9\nna\u00efve fa\u00e7ade"
    file_path.write_text(content, encoding="utf-8")
    chunks = ingest_file(str(file_path), "mixed")
    assert chunks[0].section == "1. Section"
    assert "Caf\u00e9" in chunks[0].text
