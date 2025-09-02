"""
AI-Powered Risk Analysis Router

Provides endpoints for advanced contract risk analysis including:
- Financial risk assessment
- Operational risk evaluation  
- Reputational risk analysis
- Legal risk scoring
- Overall risk profile generation
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..services.ai_risk_scorer import (
    ContractRiskProfile, 
    RiskFactor, 
    RiskLevel, 
    RiskCategory,
    ai_risk_scorer
)
from ..services.storage import get_analysis_text, get_analysis_findings

router = APIRouter(tags=["risk-analysis"])


class RiskAnalysisRequest(BaseModel):
    analysis_id: str
    include_text_analysis: bool = True
    include_findings_analysis: bool = True


class RiskAnalysisResponse(BaseModel):
    analysis_id: str
    risk_profile: ContractRiskProfile
    metadata: Dict[str, Any]


class RiskFactorResponse(BaseModel):
    category: str
    level: str
    score: float
    description: str
    evidence: str
    recommendations: List[str]
    impact: str


class ContractRiskProfileResponse(BaseModel):
    overall_score: float
    overall_level: str
    risk_factors: List[RiskFactorResponse]
    summary: str
    urgent_actions: List[str]
    monitoring_points: List[str]


@router.post("/risk-analysis", response_model=RiskAnalysisResponse)
async def analyze_contract_risk(request: RiskAnalysisRequest) -> RiskAnalysisResponse:
    """
    Perform comprehensive AI-powered risk analysis on a contract
    
    This endpoint analyzes contract risk across multiple dimensions:
    - Compliance risk (based on GDPR findings)
    - Financial risk (payment terms, penalties, high values)
    - Operational risk (SLAs, dependencies, resource commitments)
    - Reputational risk (breaches, disclosures, regulatory exposure)
    - Legal risk (jurisdiction, dispute resolution, liability)
    """
    try:
        # Get contract text if requested
        contract_text = ""
        if request.include_text_analysis:
            try:
                contract_text = get_analysis_text(request.analysis_id)
            except Exception as e:
                # Fallback to empty text if extraction fails
                contract_text = ""
        
        # Get existing findings if requested
        findings = []
        if request.include_findings_analysis:
            try:
                findings = get_analysis_findings(request.analysis_id)
            except Exception as e:
                # Fallback to empty findings if retrieval fails
                findings = []
        
        # Perform AI risk analysis
        risk_profile = ai_risk_scorer.analyze_contract_risk(contract_text, findings)
        
        # Prepare metadata
        metadata = {
            "analysis_id": request.analysis_id,
            "text_analyzed": len(contract_text) > 0,
            "findings_analyzed": len(findings) > 0,
            "risk_categories_analyzed": len(risk_profile.risk_factors),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }
        
        return RiskAnalysisResponse(
            analysis_id=request.analysis_id,
            risk_profile=risk_profile,
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Risk analysis failed: {str(e)}"
        )


@router.get("/risk-analysis/{analysis_id}", response_model=RiskAnalysisResponse)
async def get_contract_risk_analysis(
    analysis_id: str,
    include_text: bool = Query(True, description="Include text-based risk analysis"),
    include_findings: bool = Query(True, description="Include findings-based risk analysis")
) -> RiskAnalysisResponse:
    """
    Retrieve existing risk analysis for a contract
    
    If no analysis exists, performs a new one automatically.
    """
    try:
        # For now, always perform analysis (could be cached in future)
        request = RiskAnalysisRequest(
            analysis_id=analysis_id,
            include_text_analysis=include_text,
            include_findings_analysis=include_findings
        )
        
        return await analyze_contract_risk(request)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve risk analysis: {str(e)}"
        )


@router.get("/risk-analysis/{analysis_id}/summary", response_model=ContractRiskProfileResponse)
async def get_risk_summary(analysis_id: str) -> ContractRiskProfileResponse:
    """
    Get a simplified risk summary for quick assessment
    """
    try:
        # Perform full analysis
        request = RiskAnalysisRequest(
            analysis_id=analysis_id,
            include_text_analysis=True,
            include_findings_analysis=True
        )
        
        response = await analyze_contract_risk(request)
        risk_profile = response.risk_profile
        
        # Convert to response model
        risk_factors = [
            RiskFactorResponse(
                category=factor.category.value,
                level=factor.level.value,
                score=factor.score,
                description=factor.description,
                evidence=factor.evidence,
                recommendations=factor.recommendations,
                impact=factor.impact
            )
            for factor in risk_profile.risk_factors
        ]
        
        return ContractRiskProfileResponse(
            overall_score=risk_profile.overall_score,
            overall_level=risk_profile.overall_level.value,
            risk_factors=risk_factors,
            summary=risk_profile.summary,
            urgent_actions=risk_profile.urgent_actions,
            monitoring_points=risk_profile.monitoring_points
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get risk summary: {str(e)}"
        )


@router.get("/risk-analysis/{analysis_id}/urgent-actions")
async def get_urgent_actions(analysis_id: str) -> Dict[str, Any]:
    """
    Get urgent actions required for a contract
    """
    try:
        request = RiskAnalysisRequest(
            analysis_id=analysis_id,
            include_text_analysis=True,
            include_findings_analysis=True
        )
        
        response = await analyze_contract_risk(request)
        risk_profile = response.risk_profile
        
        return {
            "analysis_id": analysis_id,
            "urgent_actions": risk_profile.urgent_actions,
            "overall_risk_level": risk_profile.overall_level.value,
            "critical_factors_count": len([f for f in risk_profile.risk_factors if f.level == RiskLevel.CRITICAL]),
            "high_factors_count": len([f for f in risk_profile.risk_factors if f.level == RiskLevel.HIGH])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get urgent actions: {str(e)}"
        )


@router.get("/risk-analysis/{analysis_id}/risk-factors")
async def get_risk_factors_by_category(
    analysis_id: str,
    category: str = Query(None, description="Filter by risk category")
) -> Dict[str, Any]:
    """
    Get risk factors, optionally filtered by category
    """
    try:
        request = RiskAnalysisRequest(
            analysis_id=analysis_id,
            include_text_analysis=True,
            include_findings_analysis=True
        )
        
        response = await analyze_contract_risk(request)
        risk_profile = response.risk_profile
        
        if category:
            # Filter by category
            filtered_factors = [
                f for f in risk_profile.risk_factors 
                if f.category.value.lower() == category.lower()
            ]
        else:
            filtered_factors = risk_profile.risk_factors
        
        # Group by risk level
        risk_by_level = {}
        for factor in filtered_factors:
            level = factor.level.value
            if level not in risk_by_level:
                risk_by_level[level] = []
            
            risk_by_level[level].append({
                "category": factor.category.value,
                "score": factor.score,
                "description": factor.description,
                "evidence": factor.evidence,
                "recommendations": factor.recommendations,
                "impact": factor.impact
            })
        
        return {
            "analysis_id": analysis_id,
            "category_filter": category,
            "total_factors": len(filtered_factors),
            "risk_by_level": risk_by_level,
            "overall_risk_score": risk_profile.overall_score,
            "overall_risk_level": risk_profile.overall_level.value
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get risk factors: {str(e)}"
        )


@router.get("/risk-analysis/health")
async def risk_analysis_health() -> Dict[str, str]:
    """
    Health check for risk analysis service
    """
    return {
        "status": "healthy",
        "service": "AI Risk Analysis",
        "version": "1.0.0",
        "capabilities": [
            "Compliance Risk Assessment",
            "Financial Risk Analysis", 
            "Operational Risk Evaluation",
            "Reputational Risk Scoring",
            "Legal Risk Assessment"
        ]
    }
