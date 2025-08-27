from datetime import datetime, timedelta

import pytest

from blackletter_api.models.analysis import (
    AnalysisBase,
    AnalysisDetail,
    AnalysisListFilters,
    AnalysisListItem,
    AnalysisListResponse,
    AnalysisSort,
    AnalysisStatus,
)


def test_analysis_defaults_and_validation():
    now = datetime.utcnow()
    a = AnalysisBase(
        id="A1",
        created_at=now,
        filename="Contract.pdf",
        filesize=1234,
        status=AnalysisStatus.completed,
        findings_count=5,
        uploader="user1",
        tags=["ClientA", "Q3"],
    )
    assert a.findings_count == 5
    assert a.archived is False
    assert a.tags == ["ClientA", "Q3"]
    assert a.status == AnalysisStatus.completed

    with pytest.raises(ValueError):
        AnalysisBase(
            id="A2",
            created_at=now,
            filename="  ",
            filesize=0,
        )

    with pytest.raises(ValueError):
        AnalysisBase(
            id="A3",
            created_at=now,
            filename="ok.pdf",
            filesize=-1,
        )


def test_list_and_detail_shapes():
    now = datetime.utcnow()
    item = AnalysisListItem(
        id="A1",
        created_at=now,
        filename="a.pdf",
        filesize=1,
    )
    detail = AnalysisDetail(**item.dict())
    resp = AnalysisListResponse(items=[item], next_cursor="c1", total_estimate=100)

    assert detail.id == item.id
    assert resp.next_cursor == "c1"
    assert resp.total_estimate == 100
    assert len(resp.items) == 1


def test_filters_validation_and_defaults():
    now = datetime.utcnow()
    later = now + timedelta(days=1)

    f = AnalysisListFilters()
    assert f.limit == 25
    assert f.sort == AnalysisSort.created_at_desc

    f2 = AnalysisListFilters(
        q="clientA",
        status=["completed", AnalysisStatus.failed],
        date_from=now,
        date_to=later,
        min_findings=0,
        max_findings=10,
        limit=50,
        sort=AnalysisSort.findings_desc,
    )
    assert f2.status and AnalysisStatus.completed in f2.status
    assert f2.limit == 50
    assert f2.sort == AnalysisSort.findings_desc

    with pytest.raises(ValueError):
        AnalysisListFilters(date_from=later, date_to=now)

    with pytest.raises(ValueError):
        AnalysisListFilters(min_findings=5, max_findings=1)

