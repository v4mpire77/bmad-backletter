from __future__ import annotations

from typing import Iterable, List

from sqlalchemy import bindparam, or_, select
from sqlalchemy.orm import Session

from ..models import DocumentChunk


def search_chunks(db: Session, keywords: Iterable[str]) -> List[DocumentChunk]:
    """Return chunks whose content matches any of the given keywords.

    Keyword comparison is case-insensitive and safely parameter bound.
    """
    tokens = [kw for kw in keywords if kw]
    stmt = select(DocumentChunk)
    if not tokens:
        return list(db.execute(stmt).scalars())

    params = {}
    clauses = []
    for idx, kw in enumerate(tokens):
        param = f"kw_{idx}"
        clauses.append(DocumentChunk.content.ilike(bindparam(param)))
        params[param] = f"%{kw}%"

    stmt = stmt.where(or_(*clauses))
    return list(db.execute(stmt, params).scalars())
