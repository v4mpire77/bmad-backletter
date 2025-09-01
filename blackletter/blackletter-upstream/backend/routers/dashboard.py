from fastapi import APIRouter, UploadFile, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import uuid
from pypdf import PdfReader
from io import BytesIO
import json

from ..models.schemas import Issue

router = APIRouter()

# In-memory storage for demo purposes
# In production, this would be a database
issues_storage: List[Issue] = []

# Mock data for demonstration
MOCK_ISSUES = [
    Issue(
        id="ISS-1001",
        docId="DOC-ACME-MSA",
        docName="ACME × Blackletter — Master Services Agreement (v3)",
        clausePath="5.2 → Data Protection → International Transfers",
        type="GDPR",
        citation="UK GDPR Art. 44–49; DPA 2018 Part 2",
        severity="High",
        confidence=0.91,
        status="Open",
        snippet="Supplier may transfer Customer Personal Data outside the UK without additional safeguards.",
        recommendation="Add an international transfers clause requiring adequate safeguards (e.g., UK IDTA / Addendum, SCCs + A. Transfer Risk Assessment).",
        createdAt="2025-08-14T10:22:00Z",
    ),
    Issue(
        id="ISS-1002",
        docId="DOC-ACME-MSA",
        docName="ACME × Blackletter — Master Services Agreement (v3)",
        clausePath="5.5 → Data Protection → Subprocessors",
        type="GDPR",
        citation="UK GDPR Art. 28(2)-(4)",
        severity="Medium",
        confidence=0.84,
        status="In Review",
        owner="Omar",
        snippet="Supplier may appoint any subprocessor without prior written authorisation.",
        recommendation="Switch to prior written authorisation or at minimum provide a public subprocessor list + notice + right to object.",
        createdAt="2025-08-14T10:23:00Z",
    ),
    Issue(
        id="ISS-1003",
        docId="DOC-GAD-PA",
        docName="Government Agency — Processing Addendum",
        clausePath="2.3 → Confidentiality",
        type="Case Law",
        citation="Barclays Bank plc v Various Claimants [2020] UKSC 13 (vicarious liability scope)",
        severity="Low",
        confidence=0.73,
        status="Open",
        snippet="The clause attempts to disclaim all liability for acts of employees and contractors.",
        recommendation="Narrow liability carve-out; align with established principles on vicarious liability and statutory duties that cannot be excluded.",
        createdAt="2025-08-15T12:01:00Z",
    ),
]

# Initialize storage with mock data
if not issues_storage:
    issues_storage.extend(MOCK_ISSUES)


@router.post("/analyze", response_model=List[Issue])
async def analyze_contract(file: UploadFile):
    """Analyze a contract and return identified issues."""
    
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        # Read file content
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        # Extract text from PDF
        pdf = PdfReader(BytesIO(content))
        text_parts = []
        for page in pdf.pages:
            t = page.extract_text() or ""
            text_parts.append(t)
        text = "\n\n".join(text_parts).strip()

        if not text:
            raise HTTPException(status_code=400, detail="No extractable text found in PDF")

        # For demo purposes, create a new issue based on the uploaded file
        # In production, this would involve actual LLM analysis
        filename = file.filename or "unknown.pdf"
        new_issue = Issue(
            id=f"ISS-{str(uuid.uuid4())[:8].upper()}",
            docId=f"DOC-{filename.replace('.pdf', '').replace(' ', '-').upper()}",
            docName=filename,
            clausePath="3.2 → Data Protection → Breach Notification",
            type="GDPR",
            citation="UK GDPR Art. 33; DPA 2018 s.67",
            severity="High",
            confidence=0.89,
            status="Open",
            snippet="No clear obligation to notify the ICO within 72 hours of becoming aware of a personal data breach.",
            recommendation="Add explicit breach notification clause: 'Controller must notify ICO within 72 hours via official channels unless breach unlikely to result in risk.'",
            createdAt=datetime.utcnow().isoformat() + "Z",
        )

        # Add to storage
        issues_storage.append(new_issue)
        
        # Return the new issue
        return [new_issue]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/issues", response_model=List[Issue])
async def get_issues(
    type_filter: Optional[str] = Query(None, alias="type"),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    gdpr_focus: Optional[bool] = Query(False),
    hide_resolved: Optional[bool] = Query(False),
):
    """Get filtered list of issues."""
    
    filtered_issues = issues_storage.copy()
    
    # Apply filters
    if type_filter and type_filter != "All":
        filtered_issues = [i for i in filtered_issues if i.type == type_filter]
    
    if severity and severity != "All":
        filtered_issues = [i for i in filtered_issues if i.severity == severity]
    
    if status and status != "All":
        filtered_issues = [i for i in filtered_issues if i.status == status]
    
    if search:
        search_lower = search.lower()
        filtered_issues = [
            i for i in filtered_issues 
            if search_lower in i.docName.lower() 
            or search_lower in i.clausePath.lower() 
            or search_lower in i.snippet.lower()
        ]
    
    if gdpr_focus:
        filtered_issues = [i for i in filtered_issues if i.type == "GDPR"]
    
    if hide_resolved:
        filtered_issues = [i for i in filtered_issues if i.status != "Resolved"]
    
    return filtered_issues


@router.get("/gdpr-coverage")
async def get_gdpr_coverage():
    """Get GDPR coverage analysis."""
    return {
        "articles": {
            "hit": 15,
            "partial": 8,
            "gap": 3
        },
        "compliance_score": 0.82
    }


@router.get("/statute-coverage")
async def get_statute_coverage():
    """Get statute coverage analysis.""" 
    return {
        "statutes": {
            "dpa_2018": {"covered": 12, "total": 15},
            "pecr": {"covered": 8, "total": 10},
            "cra_2015": {"covered": 5, "total": 7}
        },
        "overall_coverage": 0.78
    }


@router.get("/caselaw")
async def get_caselaw_signals():
    """Get case law signals."""
    return {
        "relevant_cases": [
            {
                "citation": "Lloyd v Google LLC [2021] UKSC 50",
                "relevance": 0.95,
                "impact": "High"
            },
            {
                "citation": "Barclays Bank plc v Various Claimants [2020] UKSC 13",
                "relevance": 0.87,
                "impact": "Medium"
            }
        ],
        "signals_count": 23
    }


@router.post("/redlines")
async def generate_redlines(issue_id: str):
    """Generate redline suggestions for an issue."""
    
    issue = next((i for i in issues_storage if i.id == issue_id), None)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Mock redline response
    return {
        "issue_id": issue_id,
        "redlines": [
            {
                "original": issue.snippet,
                "proposed": issue.recommendation,
                "rationale": f"Based on {issue.citation}, this change ensures compliance.",
                "risk_reduction": "High"
            }
        ],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
