from __future__ import annotations
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/issues")
def list_issues():
    now = datetime.now(timezone.utc)
    iso = lambda d: d.isoformat().replace("+00:00", "Z")
    return [
        {
            "id": "ISS-1001",
            "docId": "DOC-ACME-MSA",
            "docName": "ACME × Blackletter — MSA (v3)",
            "clausePath": "5.2 → Data Protection → International Transfers",
            "type": "GDPR",
            "citation": "UK GDPR Arts. 44–49; DPA 2018 Part 2",
            "severity": "High",
            "confidence": 0.91,
            "status": "Open",
            "snippet": "Transfers outside the UK without safeguards.",
            "recommendation": "Add IDTA/Addendum or SCCs + TRA.",
            "createdAt": iso(now - timedelta(days=1)),
        }
    ]
