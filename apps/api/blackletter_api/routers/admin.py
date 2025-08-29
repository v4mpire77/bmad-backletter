from __future__ import annotations

from typing import Dict, Any, List

from fastapi import APIRouter

from ..services.token_ledger import list_all_ledgers


router = APIRouter(tags=["admin"])


@router.get("/admin/metrics")
def get_admin_metrics() -> Dict[str, Any]:
    """Expose admin metrics including tokens_per_doc per analysis.

    Response shape is intentionally simple for MVP:
    {
      "tokens_per_doc": [ { "analysis_id": "...", "total_tokens": 123, "cap": 20000, "needs_review": false } ],
      "total_analyses": 5
    }
    """
    ledgers = list_all_ledgers()
    items: List[Dict[str, Any]] = []
    for aid, ledger in ledgers.items():
        items.append(
            {
                "analysis_id": aid,
                "total_tokens": ledger.total_tokens,
                "cap": ledger.cap_per_doc,
                "needs_review": ledger.needs_review,
            }
        )
    return {
        "tokens_per_doc": items,
        "total_analyses": len(items),
    }


