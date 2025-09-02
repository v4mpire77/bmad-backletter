from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from ..services.storage import analysis_dir

router = APIRouter(tags=["exports"])


@router.get("/exports/{doc_id}.html", response_class=HTMLResponse)
def get_export_html(doc_id: str) -> HTMLResponse:
    path = analysis_dir(doc_id) / "report.html"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Export not found"},
        )
    return HTMLResponse(path.read_text(encoding="utf-8"))
