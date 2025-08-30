"""
AI-Powered Contract Risk Scoring Service

This service provides advanced risk analysis for contracts beyond basic GDPR compliance,
including financial risk, operational risk, and compliance risk scoring.
"""

from __future__ import annotations

import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(Enum):
    COMPLIANCE = "compliance"
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    REPUTATIONAL = "reputational"
    LEGAL = "legal"


@dataclass
class RiskFactor:
    category: RiskCategory
    level: RiskLevel
    score: float  # 0.0 to 1.0
    description: str
    evidence: str
    recommendations: List[str]
    impact: str


@dataclass
class ContractRiskProfile:
    overall_score: float  # 0.0 to 1.0
    overall_level: RiskLevel
    risk_factors: List[RiskFactor]
    summary: str
    urgent_actions: List[str]
    monitoring_points: List[str]


class AIRiskScorer:
    """Advanced AI-powered contract risk scoring system"""
    
    def __init__(self):
        self.risk_patterns = self._load_risk_patterns()
        self.compliance_weights = {
            RiskCategory.COMPLIANCE: 0.35,
            RiskCategory.FINANCIAL: 0.25,
            RiskCategory.OPERATIONAL: 0.20,
            RiskCategory.REPUTATIONAL: 0.15,
            RiskCategory.LEGAL: 0.05
        }
    
    def _load_risk_patterns(self) -> Dict:
        """Load risk detection patterns and rules"""
        return {
            "financial_risk": {
                "high_value_contracts": r"\b(?:million|billion|£\d+[,\d]*[km]?|€\d+[,\d]*[km]?|\$\d+[,\d]*[km]?)\b",
                "penalty_clauses": r"\b(?:penalty|liquidated damages|forfeiture|fine)\b",
                "payment_terms": r"\b(?:net\s+\d+|payment\s+within\s+\d+|advance\s+payment)\b",
                "termination_fees": r"\b(?:termination\s+fee|early\s+termination\s+cost|exit\s+charge)\b"
            },
            "operational_risk": {
                "service_levels": r"\b(?:SLA|service\s+level|uptime|availability|response\s+time)\b",
                "resource_commitments": r"\b(?:dedicated\s+staff|24/7\s+support|on-site\s+support)\b",
                "change_management": r"\b(?:change\s+request|variation|amendment|modification)\b",
                "dependency_risks": r"\b(?:single\s+point\s+of\s+failure|vendor\s+lock-in|proprietary)\b"
            },
            "reputational_risk": {
                "confidentiality_breaches": r"\b(?:data\s+breach|confidentiality\s+breach|privacy\s+violation)\b",
                "public_disclosure": r"\b(?:public\s+announcement|press\s+release|disclosure\s+obligation)\b",
                "brand_damage": r"\b(?:brand\s+damage|reputation\s+harm|public\s+relations)\b",
                "regulatory_fines": r"\b(?:ICO\s+fine|regulatory\s+penalty|enforcement\s+action)\b"
            },
            "legal_risk": {
                "jurisdiction_issues": r"\b(?:governing\s+law|jurisdiction|dispute\s+resolution)\b",
                "arbitration_clauses": r"\b(?:arbitration|mediation|alternative\s+dispute\s+resolution)\b",
                "limitation_liability": r"\b(?:limitation\s+of\s+liability|exclusion\s+clause|cap\s+on\s+damages)\b",
                "force_majeure": r"\b(?:force\s+majeure|act\s+of\s+god|unforeseen\s+circumstances)\b"
            }
        }
    
    def analyze_contract_risk(self, contract_text: str, findings: List[Dict]) -> ContractRiskProfile:
        """Analyze contract risk based on text content and existing findings"""
        
        # Extract risk factors from different categories
        risk_factors = []
        
        # Compliance risk (based on existing findings)
        compliance_risk = self._assess_compliance_risk(findings)
        risk_factors.append(compliance_risk)
        
        # Financial risk
        financial_risk = self._assess_financial_risk(contract_text)
        risk_factors.append(financial_risk)
        
        # Operational risk
        operational_risk = self._assess_operational_risk(contract_text)
        risk_factors.append(operational_risk)
        
        # Reputational risk
        reputational_risk = self._assess_reputational_risk(contract_text)
        risk_factors.append(reputational_risk)
        
        # Legal risk
        legal_risk = self._assess_legal_risk(contract_text)
        risk_factors.append(legal_risk)
        
        # Calculate overall risk score
        overall_score = self._calculate_overall_score(risk_factors)
        overall_level = self._score_to_level(overall_score)
        
        # Generate summary and recommendations
        summary = self._generate_risk_summary(risk_factors, overall_level)
        urgent_actions = self._identify_urgent_actions(risk_factors)
        monitoring_points = self._identify_monitoring_points(risk_factors)
        
        return ContractRiskProfile(
            overall_score=overall_score,
            overall_level=overall_level,
            risk_factors=risk_factors,
            summary=summary,
            urgent_actions=urgent_actions,
            monitoring_points=monitoring_points
        )
    
    def _assess_compliance_risk(self, findings: List[Dict]) -> RiskFactor:
        """Assess compliance risk based on GDPR findings"""
        if not findings:
            return RiskFactor(
                category=RiskCategory.COMPLIANCE,
                level=RiskLevel.LOW,
                score=0.1,
                description="No compliance issues detected",
                evidence="Clean analysis results",
                recommendations=["Continue monitoring for new compliance requirements"],
                impact="Minimal"
            )
        
        # Count findings by severity
        missing_count = sum(1 for f in findings if f.get("verdict") == "missing")
        weak_count = sum(1 for f in findings if f.get("verdict") == "weak")
        pass_count = sum(1 for f in findings if f.get("verdict") == "pass")
        
        total_findings = len(findings)
        
        # Calculate compliance risk score
        if missing_count > 0:
            score = 0.8 + (missing_count / total_findings) * 0.2
            level = RiskLevel.CRITICAL
            description = f"Critical compliance gaps detected: {missing_count} missing requirements"
            recommendations = [
                "Immediate review required before contract execution",
                "Consult with legal team on missing GDPR obligations",
                "Consider contract amendments or additional clauses"
            ]
        elif weak_count > 0:
            score = 0.5 + (weak_count / total_findings) * 0.3
            level = RiskLevel.HIGH
            description = f"High compliance risk: {weak_count} weak clauses identified"
            recommendations = [
                "Strengthen weak language in identified clauses",
                "Request vendor clarifications on ambiguous terms",
                "Document risk acceptance if proceeding"
            ]
        else:
            score = 0.1 + (pass_count / total_findings) * 0.2
            level = RiskLevel.LOW
            description = "Good compliance posture with minor areas for improvement"
            recommendations = ["Monitor for regulatory changes", "Regular compliance reviews"]
        
        return RiskFactor(
            category=RiskCategory.COMPLIANCE,
            level=level,
            score=min(score, 1.0),
            description=description,
            evidence=f"Analysis found {missing_count} missing, {weak_count} weak, {pass_count} compliant clauses",
            recommendations=recommendations,
            impact="High" if level in [RiskLevel.HIGH, RiskLevel.CRITICAL] else "Medium"
        )
    
    def _assess_financial_risk(self, contract_text: str) -> RiskFactor:
        """Assess financial risk from contract terms"""
        text_lower = contract_text.lower()
        
        # Check for high-value indicators
        high_value_matches = re.findall(self.risk_patterns["financial_risk"]["high_value_contracts"], contract_text, re.IGNORECASE)
        penalty_matches = re.findall(self.risk_patterns["financial_risk"]["penalty_clauses"], text_lower)
        payment_matches = re.findall(self.risk_patterns["financial_risk"]["payment_terms"], text_lower)
        
        # Calculate financial risk score
        risk_score = 0.1  # Base score
        
        if high_value_matches:
            risk_score += 0.3
        if penalty_matches:
            risk_score += 0.2
        if payment_matches:
            risk_score += 0.1
        
        # Determine risk level
        if risk_score >= 0.7:
            level = RiskLevel.HIGH
            description = "High financial exposure identified"
            recommendations = [
                "Review financial commitments and payment terms",
                "Assess penalty clause implications",
                "Consider financial risk insurance"
            ]
        elif risk_score >= 0.4:
            level = RiskLevel.MEDIUM
            description = "Moderate financial risk exposure"
            recommendations = [
                "Monitor payment obligations",
                "Review penalty clause triggers"
            ]
        else:
            level = RiskLevel.LOW
            description = "Low financial risk exposure"
            recommendations = ["Standard financial monitoring"]
        
        return RiskFactor(
            category=RiskCategory.FINANCIAL,
            level=level,
            score=risk_score,
            description=description,
            evidence=f"Found {len(high_value_matches)} high-value indicators, {len(penalty_matches)} penalty clauses",
            recommendations=recommendations,
            impact="High" if level == RiskLevel.HIGH else "Medium"
        )
    
    def _assess_operational_risk(self, contract_text: str) -> RiskFactor:
        """Assess operational risk from contract terms"""
        text_lower = contract_text.lower()
        
        # Check operational risk indicators
        sla_matches = re.findall(self.risk_patterns["operational_risk"]["service_levels"], text_lower)
        resource_matches = re.findall(self.risk_patterns["operational_risk"]["resource_commitments"], text_lower)
        dependency_matches = re.findall(self.risk_patterns["operational_risk"]["dependency_risks"], text_lower)
        
        risk_score = 0.1
        
        if sla_matches:
            risk_score += 0.2
        if resource_matches:
            risk_score += 0.2
        if dependency_matches:
            risk_score += 0.3
        
        if risk_score >= 0.6:
            level = RiskLevel.HIGH
            description = "High operational dependency risk"
            recommendations = [
                "Assess vendor capability to meet SLAs",
                "Plan for resource commitment requirements",
                "Develop contingency plans for dependencies"
            ]
        elif risk_score >= 0.3:
            level = RiskLevel.MEDIUM
            description = "Moderate operational risk"
            recommendations = [
                "Monitor SLA performance",
                "Track resource commitments"
            ]
        else:
            level = RiskLevel.LOW
            description = "Low operational risk"
            recommendations = ["Standard operational monitoring"]
        
        return RiskFactor(
            category=RiskCategory.OPERATIONAL,
            level=level,
            score=risk_score,
            description=description,
            evidence=f"Found {len(sla_matches)} SLA references, {len(resource_matches)} resource commitments",
            recommendations=recommendations,
            impact="High" if level == RiskLevel.HIGH else "Medium"
        )
    
    def _assess_reputational_risk(self, contract_text: str) -> RiskFactor:
        """Assess reputational risk from contract terms"""
        text_lower = contract_text.lower()
        
        breach_matches = re.findall(self.risk_patterns["reputational_risk"]["confidentiality_breaches"], text_lower)
        disclosure_matches = re.findall(self.risk_patterns["reputational_risk"]["public_disclosure"], text_lower)
        regulatory_matches = re.findall(self.risk_patterns["reputational_risk"]["regulatory_fines"], text_lower)
        
        risk_score = 0.1
        
        if breach_matches:
            risk_score += 0.3
        if disclosure_matches:
            risk_score += 0.2
        if regulatory_matches:
            risk_score += 0.2
        
        if risk_score >= 0.6:
            level = RiskLevel.HIGH
            description = "High reputational risk exposure"
            recommendations = [
                "Review confidentiality and disclosure obligations",
                "Assess regulatory compliance requirements",
                "Develop crisis communication plan"
            ]
        elif risk_score >= 0.3:
            level = RiskLevel.MEDIUM
            description = "Moderate reputational risk"
            recommendations = [
                "Monitor disclosure obligations",
                "Review confidentiality terms"
            ]
        else:
            level = RiskLevel.LOW
            description = "Low reputational risk"
            recommendations = ["Standard reputation monitoring"]
        
        return RiskFactor(
            category=RiskCategory.REPUTATIONAL,
            level=level,
            score=risk_score,
            description=description,
            evidence=f"Found {len(breach_matches)} breach references, {len(disclosure_matches)} disclosure obligations",
            recommendations=recommendations,
            impact="High" if level == RiskLevel.HIGH else "Medium"
        )
    
    def _assess_legal_risk(self, contract_text: str) -> RiskFactor:
        """Assess legal risk from contract terms"""
        text_lower = contract_text.lower()
        
        jurisdiction_matches = re.findall(self.risk_patterns["legal_risk"]["jurisdiction_issues"], text_lower)
        arbitration_matches = re.findall(self.risk_patterns["legal_risk"]["arbitration_clauses"], text_lower)
        liability_matches = re.findall(self.risk_patterns["legal_risk"]["limitation_liability"], text_lower)
        
        risk_score = 0.1
        
        if jurisdiction_matches:
            risk_score += 0.2
        if arbitration_matches:
            risk_score += 0.2
        if liability_matches:
            risk_score += 0.2
        
        if risk_score >= 0.5:
            level = RiskLevel.HIGH
            description = "High legal risk exposure"
            recommendations = [
                "Review jurisdiction and governing law clauses",
                "Assess dispute resolution mechanisms",
                "Consult with legal counsel on liability terms"
            ]
        elif risk_score >= 0.3:
            level = RiskLevel.MEDIUM
            description = "Moderate legal risk"
            recommendations = [
                "Review dispute resolution terms",
                "Assess liability limitations"
            ]
        else:
            level = RiskLevel.LOW
            description = "Low legal risk"
            recommendations = ["Standard legal review"]
        
        return RiskFactor(
            category=RiskCategory.LEGAL,
            level=level,
            score=risk_score,
            description=description,
            evidence=f"Found {len(jurisdiction_matches)} jurisdiction references, {len(arbitration_matches)} dispute resolution clauses",
            recommendations=recommendations,
            impact="High" if level == RiskLevel.HIGH else "Medium"
        )
    
    def _calculate_overall_score(self, risk_factors: List[RiskFactor]) -> float:
        """Calculate weighted overall risk score"""
        weighted_score = 0.0
        
        for factor in risk_factors:
            weight = self.compliance_weights.get(factor.category, 0.1)
            weighted_score += factor.score * weight
        
        return min(weighted_score, 1.0)
    
    def _score_to_level(self, score: float) -> RiskLevel:
        """Convert numerical score to risk level"""
        if score >= 0.8:
            return RiskLevel.CRITICAL
        elif score >= 0.6:
            return RiskLevel.HIGH
        elif score >= 0.4:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_risk_summary(self, risk_factors: List[RiskFactor], overall_level: RiskLevel) -> str:
        """Generate human-readable risk summary"""
        critical_factors = [f for f in risk_factors if f.level == RiskLevel.CRITICAL]
        high_factors = [f for f in risk_factors if f.level == RiskLevel.HIGH]
        
        if critical_factors:
            return f"CRITICAL RISK: {len(critical_factors)} critical risk factors identified. Immediate action required before contract execution."
        elif high_factors:
            return f"HIGH RISK: {len(high_factors)} high-risk areas identified. Significant review and mitigation required."
        elif overall_level == RiskLevel.MEDIUM:
            return "MEDIUM RISK: Several areas require attention and monitoring. Proceed with caution and regular reviews."
        else:
            return "LOW RISK: Contract appears to have acceptable risk profile. Standard monitoring recommended."
    
    def _identify_urgent_actions(self, risk_factors: List[RiskFactor]) -> List[str]:
        """Identify urgent actions required"""
        urgent_actions = []
        
        for factor in risk_factors:
            if factor.level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                urgent_actions.extend(factor.recommendations[:2])  # Top 2 recommendations
        
        # Remove duplicates and limit to top 5
        unique_actions = list(dict.fromkeys(urgent_actions))
        return unique_actions[:5]
    
    def _identify_monitoring_points(self, risk_factors: List[RiskFactor]) -> List[str]:
        """Identify key monitoring points"""
        monitoring_points = []
        
        for factor in risk_factors:
            if factor.level in [RiskLevel.MEDIUM, RiskLevel.HIGH]:
                monitoring_points.append(f"Monitor {factor.category.value} risk indicators")
        
        return monitoring_points


# Global instance
ai_risk_scorer = AIRiskScorer()
