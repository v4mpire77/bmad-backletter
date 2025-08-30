from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from blackletter_api.database import Base
from blackletter_api.models import DocumentChunk
from blackletter_api.services.chunk_search import search_chunks


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        session.add_all(
            [
                DocumentChunk(content="The quick brown fox"),
                DocumentChunk(content="Lazy Dog leaps over"),
                DocumentChunk(content="Something unrelated"),
            ]
        )
        session.commit()
        yield session


def test_search_chunks_matches_keywords(db_session: Session) -> None:
    results = search_chunks(db_session, ["fox", "dog"])
    contents = {chunk.content for chunk in results}
    assert contents == {"The quick brown fox", "Lazy Dog leaps over"}


def test_search_chunks_handles_empty_keywords(db_session: Session) -> None:
    results = search_chunks(db_session, [])
    assert len(results) == 3
