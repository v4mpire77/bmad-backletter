from __future__ import annotations
from typing import List
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

# Import your ORM model
try:
    from apps.api.blackletter_api.models import DocumentChunk  # adjust if different
except Exception:  # fallback for some test layouts
    from blackletter_api.models import DocumentChunk  # type: ignore


def search_chunks(session: Session, keywords: List[str]) -> List["DocumentChunk"]:
    """
    Simple LIKE-based search. Handles empty keywords and uses the provided Session.
    Tests create the schema/fixtures; we just query safely.
    """
    kw = [k.strip() for k in (keywords or []) if k and k.strip()]
    if not kw:
        stmt = select(DocumentChunk)
        return list(session.execute(stmt).scalars().all())

    conditions = [DocumentChunk.text.ilike(f"%{k}%") for k in kw]
    stmt = select(DocumentChunk).where(or_(*conditions))
    return list(session.execute(stmt).scalars().all())

