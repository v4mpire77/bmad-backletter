from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("/gdpr-coverage")
def gdpr_coverage(docId: str | None = None):
    return [
        {"article": "Art. 5 — Principles", "status": "OK"},
        {"article": "Art. 6 — Lawfulness", "status": "OK"},
        {"article": "Art. 28 — Processor", "status": "GAP"},
        {"article": "Art. 32 — Security", "status": "OK"},
        {"article": "Arts. 44–49 — Transfers", "status": "GAP"},
        {"article": "Art. 30 — Records", "status": "Partial"},
    ]

@router.get("/statute-coverage")
def statute_coverage(docId: str | None = None):
    return [
        {"ref": "DPA 2018 Part 2", "status": "Partial"},
        {"ref": "PECR 2003 (as amended)", "status": "OK"},
        {"ref": "Consumer Rights Act 2015", "status": "Review"},
    ]

@router.get("/caselaw")
def case_law(docId: str | None = None):
    return [
        {"case": "Barclays v Various Claimants [2020] UKSC 13", "weight": 0.8},
        {"case": "Lloyd v Google [2021] UKSC 50", "weight": 0.7},
        {"case": "NT1 & NT2 v Google [2018] EWCA Civ 799", "weight": 0.6},
    ]
