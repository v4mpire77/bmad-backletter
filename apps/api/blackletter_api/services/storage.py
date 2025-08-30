from __future__ import annotations

from pathlib import Path
from typing import Final

from fastapi import UploadFile


BASE_DIR: Final[Path] = Path(__file__).resolve().parents[1]
STORAGE_DIR: Final[Path] = BASE_DIR / "_storage"
STORAGE_DIR.mkdir(exist_ok=True)


async def save_upload(file: UploadFile) -> Path:
    """Persist the uploaded file and return its path.

    Keeps the original filename only; does not log or return content.
    """
    target = STORAGE_DIR / file.filename
    # Ensure unique by suffixing if exists
    i = 1
    stem = target.stem
    suffix = target.suffix
    while target.exists():
        target = STORAGE_DIR / f"{stem}_{i}{suffix}"
        i += 1

    with target.open("wb") as fh:
        while True:
            chunk = await file.read(1024 * 256)
            if not chunk:
                break
            fh.write(chunk)

    # Rewind the UploadFile stream so other consumers can still read if needed
    try:
        file.file.seek(0)
    except Exception:
        pass

    return target

