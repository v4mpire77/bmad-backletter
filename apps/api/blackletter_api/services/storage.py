from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, List

from fastapi import UploadFile
import json

from ..models.schemas import AnalysisSummary, VerdictCounts


DATA_ROOT = Path(os.getenv("DATA_ROOT", ".data")).resolve()


def analysis_dir(analysis_id: str) -> Path:
    d = DATA_ROOT / "analyses" / analysis_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def sanitize_filename(name: str) -> str:
    # Drop any directory components and strip dangerous characters
    base = os.path.basename(name).strip().replace("\x00", "")
    # Avoid empty filenames
    return base or "upload"


def save_upload(file: UploadFile, dest: Path, max_bytes: int = 10 * 1024 * 1024) -> int:
    total = 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as f:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                # Truncate/cleanup and raise
                try:
                    # Ensure file handle is closed before unlink on Windows
                    f.flush()
                finally:
                    try:
                        f.close()
                    except Exception:
                        pass
                    try:
                        dest.unlink(missing_ok=True)
                    except FileNotFoundError:
                        pass
                raise ValueError("file_too_large")
            f.write(chunk)
    return total


def write_analysis_json(analysis_id: str, filename: str, size: int) -> Path:
    d = analysis_dir(analysis_id)
    payload = {
        "id": analysis_id,
        "filename": filename,
        "size": size,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "done",
    }
    p = d / "analysis.json"
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f)
    return p


def _parse_iso(dt: str) -> float:
    try:
        # Python 3.11+ supports fromisoformat with Z? Use replace as needed
        return datetime.fromisoformat(dt.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def load_analysis_summary(analysis_id: str) -> AnalysisSummary | None:
    """Load a persisted analysis.json and return an AnalysisSummary.

    Returns None if the analysis cannot be loaded.
    """
    p = analysis_dir(analysis_id) / "analysis.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    return AnalysisSummary(
        id=str(data.get("id") or analysis_id),
        filename=str(data.get("filename") or "unknown"),
        created_at=str(data.get("created_at") or datetime.now(timezone.utc).isoformat()),
        size=int(data.get("size") or 0),
        state=str(data.get("status") or "REPORTED"),
        verdicts=VerdictCounts(),
    )


def list_analyses_summaries(limit: int = 50) -> List[AnalysisSummary]:
    """Scan DATA_ROOT/analyses/*/analysis.json and return up to `limit` summaries."""
    root = DATA_ROOT / "analyses"
    if not root.exists():
        return []
    items: List[AnalysisSummary] = []
    for d in root.iterdir():
        if not d.is_dir():
            continue
        p = d / "analysis.json"
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        try:
            items.append(
                AnalysisSummary(
                    id=str(data.get("id") or d.name),
                    filename=str(data.get("filename") or "unknown"),
                    created_at=str(data.get("created_at") or datetime.now(timezone.utc).isoformat()),
                    size=int(data.get("size") or 0),
                    state=str(data.get("status") or "REPORTED"),
                    verdicts=VerdictCounts(),
                )
            )
        except Exception:
            # Skip corrupt entries
            continue

    # Sort by created_at desc if available
    items.sort(key=lambda x: _parse_iso(x.created_at), reverse=True)
    return items[: max(0, int(limit))]
