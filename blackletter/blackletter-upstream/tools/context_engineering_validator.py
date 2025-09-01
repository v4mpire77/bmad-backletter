#!/usr/bin/env python3
"""
Context Engineering Workflow Validator

This tool validates that agents are following the Context Engineering workflow
by checking their responses against the mandatory workflow requirements.
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextEngineeringValidator:
    """
    Validates agent responses against the Context Engineering workflow requirements.
    """
    
    def __init__(self):
        self.workflow_steps = [
            "Context Assessment",
            "Implementation Plan", 
            "Implementation",
            "Documentation",
            "Verification against checklist"
        ]
        
        self.critical_rules = {
            "NEVER": [
                "ignore the Context Engineering workflow",
                "hardcode API keys or secrets",
                "write to local disk for artifacts",
                "embed PDFs without chunking",
                "implement features without consulting documentation first",
                "leave code in a broken state",
                "commit code that doesn't follow established patterns"
            ],
            "ALWAYS": [
                "follow the workflow sequence",
                "keep adapters vendor-agnostic",
                "write tests for core functionality",
                "include proper error handling",
                "use existing components and utilities",
                "follow naming conventions",
                "document your code",
                "consider security implications"
            ]
        }
        
        self.required_docs = [
            "docs/Implementation.md",
            "docs/project_structure.md", 
            "docs/UI_UX_doc.md",
            "docs/Bug_tracking.md"
        ]
    
    def validate_response(self, response_text: str) -> Dict[str, any]:
        """
        Validate an agent's response against the Context Engineering workflow.
        
        Args:
            response_text: The agent's response text to validate
            
        Returns:
            Dict containing validation results and recommendations
        """
        results = {
            "workflow_compliance": self._check_workflow_steps(response_text),
            "documentation_references": self._check_documentation_references(response_text),
            "rule_compliance": self._check_rule_compliance(response_text),
            "overall_score": 0,
            "recommendations": [],
            "passed": False
        }
        
        # Calculate overall score
        workflow_score = len(results["workflow_compliance"]["found"]) / len(self.workflow_steps) * 100
        docs_score = len(results["documentation_references"]["found"]) / len(self.required_docs) * 100
        rules_score = results["rule_compliance"]["score"]
        
        results["overall_score"] = (workflow_score + docs_score + rules_score) / 3
        results["passed"] = results["overall_score"] >= 80
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)
        
        return results
    
    def _check_workflow_steps(self, response_text: str) -> Dict[str, any]:
        """Check if all required workflow steps are present."""
        found_steps = []
        missing_steps = []
        
        for step in self.workflow_steps:
            if re.search(rf"\b{re.escape(step)}\b", response_text, re.IGNORECASE):
                found_steps.append(step)
            else:
                missing_steps.append(step)
        
        return {
            "found": found_steps,
            "missing": missing_steps,
            "complete": len(missing_steps) == 0
        }
    
    def _check_documentation_references(self, response_text: str) -> Dict[str, any]:
        """Check if required documentation files are referenced."""
        found_docs = []
        missing_docs = []
        
        for doc in self.required_docs:
            if re.search(rf"\b{re.escape(doc)}\b", response_text):
                found_docs.append(doc)
            else:
                missing_docs.append(doc)
        
        return {
            "found": found_docs,
            "missing": missing_docs,
            "complete": len(missing_docs) == 0
        }
    
    def _check_rule_compliance(self, response_text: str) -> Dict[str, any]:
        """Check compliance with critical rules."""
        violations = []
        compliance_score = 100
        
        # Check NEVER rules
        for rule in self.critical_rules["NEVER"]:
            if re.search(rf"\b{re.escape(rule)}\b", response_text, re.IGNORECASE):
                violations.append(f"NEVER: {rule}")
                compliance_score -= 10
        
        # Check ALWAYS rules (looking for positive mentions)
        always_found = 0
        for rule in self.critical_rules["ALWAYS"]:
            if re.search(rf"\b{re.escape(rule)}\b", response_text, re.IGNORECASE):
                always_found += 1
        
        always_score = (always_found / len(self.critical_rules["ALWAYS"])) * 100
        compliance_score = (compliance_score + always_score) / 2
        
        return {
            "violations": violations,
            "always_rules_found": always_found,
            "score": max(0, compliance_score)
        }
    
    def _generate_recommendations(self, results: Dict[str, any]) -> List[str]:
        """Generate specific recommendations for improvement."""
        recommendations = []
        
        # Workflow recommendations
        if not results["workflow_compliance"]["complete"]:
            missing = ", ".join(results["workflow_compliance"]["missing"])
            recommendations.append(f"Missing workflow steps: {missing}")
            recommendations.append("Ensure your response follows the Context Engineering workflow structure")
        
        # Documentation recommendations
        if not results["documentation_references"]["complete"]:
            missing = ", ".join(results["documentation_references"]["missing"])
            recommendations.append(f"Missing documentation references: {missing}")
            recommendations.append("Always consult the required documentation files before implementation")
        
        # Rule compliance recommendations
        if results["rule_compliance"]["violations"]:
            violations = "; ".join(results["rule_compliance"]["violations"])
            recommendations.append(f"Rule violations detected: {violations}")
            recommendations.append("Review and correct any violations of the critical rules")
        
        if results["rule_compliance"]["score"] < 80:
            recommendations.append("Improve compliance with ALWAYS rules")
            recommendations.append("Ensure all critical requirements are addressed")
        
        # General recommendations
        if results["overall_score"] < 80:
            recommendations.append("Review the Context Engineering workflow documentation")
            recommendations.append("Follow the complete workflow sequence: Context → Implementation → Documentation")
        
        return recommendations
    
    def generate_report(self, validation_results: Dict[str, any]) -> str:
        """Generate a human-readable validation report."""
        report = []
        report.append("=" * 60)
        report.append("CONTEXT ENGINEERING WORKFLOW VALIDATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Overall score
        score = validation_results["overall_score"]
        status = "✅ PASSED" if validation_results["passed"] else "❌ FAILED"
        report.append(f"Overall Score: {score:.1f}% {status}")
        report.append("")
        
        # Workflow compliance
        workflow = validation_results["workflow_compliance"]
        report.append("📋 WORKFLOW COMPLIANCE")
        report.append(f"Status: {'✅ Complete' if workflow['complete'] else '❌ Incomplete'}")
        report.append(f"Found: {len(workflow['found'])}/{len(self.workflow_steps)} steps")
        if workflow['missing']:
            report.append(f"Missing: {', '.join(workflow['missing'])}")
        report.append("")
        
        # Documentation references
        docs = validation_results["documentation_references"]
        report.append("📚 DOCUMENTATION REFERENCES")
        report.append(f"Status: {'✅ Complete' if docs['complete'] else '❌ Incomplete'}")
        report.append(f"Referenced: {len(docs['found'])}/{len(self.required_docs)} files")
        if docs['missing']:
            report.append(f"Missing: {', '.join(docs['missing'])}")
        report.append("")
        
        # Rule compliance
        rules = validation_results["rule_compliance"]
        report.append("🔒 RULE COMPLIANCE")
        report.append(f"Score: {rules['score']:.1f}%")
        report.append(f"ALWAYS Rules Found: {rules['always_rules_found']}/{len(self.critical_rules['ALWAYS'])}")
        if rules['violations']:
            report.append(f"Violations: {len(rules['violations'])}")
            for violation in rules['violations']:
                report.append(f"  - {violation}")
        report.append("")
        
        # Recommendations
        if validation_results["recommendations"]:
            report.append("💡 RECOMMENDATIONS")
            for rec in validation_results["recommendations"]:
                report.append(f"• {rec}")
            report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)

def main():
    """CLI interface for the validator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Context Engineering workflow compliance")
    parser.add_argument("input", help="Input file containing agent response or '-' for stdin")
    parser.add_argument("--output", "-o", help="Output file for validation report")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    # Read input
    if args.input == "-":
        response_text = input("Paste the agent response: ")
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            response_text = f.read()
    
    # Validate
    validator = ContextEngineeringValidator()
    results = validator.validate_response(response_text)
    
    # Generate output
    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output = validator.generate_report(results)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Validation report written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
