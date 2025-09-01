#!/usr/bin/env python3
"""
BMAD-Enhanced Context Engineering Workflow Validator

This tool validates that agents are following the BMAD-enhanced Context Engineering workflow
by checking their responses against the mandatory workflow requirements, including BMAD
business context assessment, risk management, and advanced elicitation techniques.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BMADContextEngineeringValidator:
    """
    Validates agent responses against the BMAD-enhanced Context Engineering workflow requirements.
    """

    def __init__(self):
        self.workflow_steps = [
            "Business Context Assessment",
            "Technical Context Assessment",
            "Risk and Compatibility Analysis",
            "Code Implementation",
            "Documentation",
            "Verification against checklist",
        ]

        self.bmad_enhanced_steps = [
            "Business Value Focus",
            "Advanced Elicitation Techniques",
            "Knowledge Transfer Documentation",
        ]

        self.critical_rules = {
            "NEVER": [
                "ignore the Context Engineering workflow",
                "hardcode API keys or secrets",
                "write to local disk for artifacts",
                "embed PDFs without chunking",
                "implement features without consulting documentation first",
                "leave code in a broken state",
                "commit code that doesn't follow established patterns",
                "proceed without understanding business context",
                "ignore risk assessment requirements",
                "skip advanced elicitation when working on significant features",
            ],
            "ALWAYS": [
                "follow the workflow sequence",
                "keep adapters vendor-agnostic",
                "write tests for core functionality",
                "include proper error handling",
                "use existing components and utilities",
                "follow naming conventions",
                "document your code",
                "consider security implications",
                "analyze business context and stakeholder needs",
                "assess risks and document mitigation strategies",
                "include business logic documentation",
                "validate implementation against business success criteria",
                "document business value delivered by implementations",
                "apply advanced elicitation techniques for deeper exploration of ideas",
                "document insights gained through advanced elicitation",
            ],
        }

        self.required_docs = [
            "docs/Business_Requirements.md",
            "docs/Business_Value_Assessment.md",
            "docs/Implementation.md",
            "docs/project_structure.md",
            "docs/UI_UX_doc.md",
            "docs/Bug_tracking.md",
            "docs/ARCHITECTURE.md",
            "docs/Risk_Management_Framework.md",
        ]

        self.bmad_advanced_elicitation_methods = [
            "Expand/Contract for Audience",
            "Critique and Refine",
            "Identify Potential Risks",
            "Assess Alignment with Goals",
            "Tree of Thoughts",
            "ReWOO",
            "Meta-Prompting",
            "Agile Team Perspective",
            "Stakeholder Roundtable",
            "Innovation Tournament",
            "Escape Room Challenge",
            "Red Team vs Blue Team",
            "Hindsight Reflection",
        ]

    def validate_response(self, response_text: str) -> Dict[str, any]:
        """
        Validate an agent's response against the BMAD-enhanced Context Engineering workflow.

        Args:
            response_text: The agent's response text to validate

        Returns:
            Dict containing validation results and recommendations
        """
        results = {
            "workflow_compliance": self._check_workflow_steps(response_text),
            "bmad_enhancement_compliance": self._check_bmad_enhancement_steps(
                response_text
            ),
            "documentation_references": self._check_documentation_references(
                response_text
            ),
            "rule_compliance": self._check_rule_compliance(response_text),
            "advanced_elicitation_compliance": self._check_advanced_elicitation_compliance(
                response_text
            ),
            "business_value_documentation": self._check_business_value_documentation(
                response_text
            ),
            "knowledge_transfer_documentation": self._check_knowledge_transfer_documentation(
                response_text
            ),
            "overall_score": 0,
            "recommendations": [],
            "passed": False,
        }

        # Calculate overall score
        workflow_score = (
            len(results["workflow_compliance"]["found"])
            / len(self.workflow_steps)
            * 100
        )
        bmad_score = (
            len(results["bmad_enhancement_compliance"]["found"])
            / len(self.bmad_enhanced_steps)
            * 100
        )
        docs_score = (
            len(results["documentation_references"]["found"])
            / len(self.required_docs)
            * 100
        )
        rules_score = results["rule_compliance"]["score"]
        elicitation_score = results["advanced_elicitation_compliance"]["score"]
        business_value_score = results["business_value_documentation"]["score"]
        knowledge_transfer_score = results["knowledge_transfer_documentation"]["score"]

        # Weighted scoring: workflow (20%), BMAD enhancement (20%), docs (15%), rules (15%),
        # elicitation (10%), business value (10%), knowledge transfer (10%)
        results["overall_score"] = (
            workflow_score * 0.2
            + bmad_score * 0.2
            + docs_score * 0.15
            + rules_score * 0.15
            + elicitation_score * 0.1
            + business_value_score * 0.1
            + knowledge_transfer_score * 0.1
        )

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
            "complete": len(missing_steps) == 0,
        }

    def _check_bmad_enhancement_steps(self, response_text: str) -> Dict[str, any]:
        """Check if BMAD-enhanced workflow steps are present."""
        found_steps = []
        missing_steps = []

        for step in self.bmad_enhanced_steps:
            # Check for the step name or related keywords
            patterns = [
                rf"\b{re.escape(step)}\b",
                (
                    rf"\bbusiness.*{re.escape(step.split()[-1])}\b"
                    if "business" not in step.lower()
                    else rf"\b{re.escape(step)}\b"
                ),
            ]

            found = False
            for pattern in patterns:
                if re.search(pattern, response_text, re.IGNORECASE):
                    found = True
                    break

            if found:
                found_steps.append(step)
            else:
                missing_steps.append(step)

        return {
            "found": found_steps,
            "missing": missing_steps,
            "complete": len(missing_steps) == 0,
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
            "complete": len(missing_docs) == 0,
        }

    def _check_rule_compliance(self, response_text: str) -> Dict[str, any]:
        """Check compliance with critical rules."""
        violations = []
        compliance_score = 100

        # Check NEVER rules
        for rule in self.critical_rules["NEVER"]:
            if re.search(rf"\b{re.escape(rule)}\b", response_text, re.IGNORECASE):
                violations.append(f"NEVER: {rule}")
                compliance_score -= (
                    8  # Reduced penalty to avoid going below 0 too quickly
                )

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
            "score": max(0, compliance_score),
        }

    def _check_advanced_elicitation_compliance(
        self, response_text: str
    ) -> Dict[str, any]:
        """Check if advanced elicitation techniques are properly applied."""
        found_methods = []
        missing_methods = []

        # Check for mentions of advanced elicitation methods
        for method in self.bmad_advanced_elicitation_methods:
            if re.search(rf"\b{re.escape(method)}\b", response_text, re.IGNORECASE):
                found_methods.append(method)

        # If we found some methods, we consider this partially complete
        # In a real implementation, we would check for proper application
        method_score = min(
            100,
            (len(found_methods) / len(self.bmad_advanced_elicitation_methods)) * 100,
        )

        return {
            "found": found_methods,
            "missing": missing_methods,  # We don't actually track missing since we're looking for mentions
            "score": method_score,
            "complete": len(found_methods) > 0,
        }

    def _check_business_value_documentation(self, response_text: str) -> Dict[str, any]:
        """Check if business value documentation is present."""
        business_value_indicators = [
            r"business\s+value",
            r"stakeholder\s+impact",
            r"user\s+experience",
            r"revenue.*implication",
            r"cost.*implication",
            r"success\s+criteria",
            r"performance\s+metric",
            r"business\s+requirement",
            r"strategic\s+alignment",
        ]

        found_indicators = []
        for indicator in business_value_indicators:
            if re.search(indicator, response_text, re.IGNORECASE):
                found_indicators.append(indicator)

        # Score based on number of indicators found
        score = min(100, (len(found_indicators) / len(business_value_indicators)) * 100)

        return {
            "found": found_indicators,
            "score": score,
            "complete": len(found_indicators)
            > 3,  # At least 3 indicators should be present
        }

    def _check_knowledge_transfer_documentation(
        self, response_text: str
    ) -> Dict[str, any]:
        """Check if knowledge transfer documentation is present."""
        knowledge_transfer_indicators = [
            r"lesson\s+learned",
            r"architectural\s+decision",
            r"technical\s+debt",
            r"implementation\s+challenge",
            r"solution.*approach",
            r"future\s+improvement",
            r"insight.*gain",
            r"elicitation.*result",
        ]

        found_indicators = []
        for indicator in knowledge_transfer_indicators:
            if re.search(indicator, response_text, re.IGNORECASE):
                found_indicators.append(indicator)

        # Score based on number of indicators found
        score = min(
            100, (len(found_indicators) / len(knowledge_transfer_indicators)) * 100
        )

        return {
            "found": found_indicators,
            "score": score,
            "complete": len(found_indicators)
            > 2,  # At least 2 indicators should be present
        }

    def _generate_recommendations(self, results: Dict[str, any]) -> List[str]:
        """Generate specific recommendations for improvement."""
        recommendations = []

        # Workflow recommendations
        if not results["workflow_compliance"]["complete"]:
            missing = ", ".join(results["workflow_compliance"]["missing"])
            recommendations.append(f"Missing workflow steps: {missing}")
            recommendations.append(
                "Ensure your response follows the complete Context Engineering workflow structure"
            )

        # BMAD enhancement recommendations
        if not results["bmad_enhancement_compliance"]["complete"]:
            missing = ", ".join(results["bmad_enhancement_compliance"]["missing"])
            recommendations.append(f"Missing BMAD enhancements: {missing}")
            recommendations.append(
                "Incorporate BMAD business context assessment, risk management, and advanced elicitation techniques"
            )

        # Documentation recommendations
        if not results["documentation_references"]["complete"]:
            missing = ", ".join(results["documentation_references"]["missing"])
            recommendations.append(f"Missing documentation references: {missing}")
            recommendations.append(
                "Always consult the required documentation files before implementation, especially business requirements and risk management documents"
            )

        # Rule compliance recommendations
        if results["rule_compliance"]["violations"]:
            violations = "; ".join(results["rule_compliance"]["violations"])
            recommendations.append(f"Rule violations detected: {violations}")
            recommendations.append(
                "Review and correct any violations of the critical rules"
            )

        if results["rule_compliance"]["score"] < 80:
            recommendations.append(
                "Improve compliance with ALWAYS rules, particularly those related to business context and risk assessment"
            )
            recommendations.append("Ensure all critical requirements are addressed")

        # Advanced elicitation recommendations
        if not results["advanced_elicitation_compliance"]["complete"]:
            recommendations.append(
                "Apply advanced elicitation techniques to validate design decisions and explore alternative approaches"
            )
            recommendations.append(
                "Document insights gained through advanced elicitation sessions"
            )

        # Business value documentation recommendations
        if not results["business_value_documentation"]["complete"]:
            recommendations.append(
                "Document business value delivered by implementations"
            )
            recommendations.append(
                "Link implementation to specific business requirements and success metrics"
            )
            recommendations.append(
                "Capture any insights about business impact during implementation"
            )

        # Knowledge transfer recommendations
        if not results["knowledge_transfer_documentation"]["complete"]:
            recommendations.append("Document lessons learned during implementation")
            recommendations.append("Capture architectural decisions and rationale")
            recommendations.append(
                "Record insights gained through advanced elicitation techniques"
            )

        # General recommendations
        if results["overall_score"] < 80:
            recommendations.append(
                "Review the BMAD-enhanced Context Engineering workflow documentation"
            )
            recommendations.append(
                "Follow the complete workflow sequence: Business Context → Technical Context → Risk Analysis → Implementation → Documentation"
            )
            recommendations.append(
                "Ensure BMAD principles are integrated throughout the development process"
            )

        return recommendations

    def generate_report(self, validation_results: Dict[str, any]) -> str:
        """Generate a human-readable validation report."""
        report = []
        report.append("=" * 70)
        report.append("BMAD-ENHANCED CONTEXT ENGINEERING WORKFLOW VALIDATION REPORT")
        report.append("=" * 70)
        report.append("")

        # Overall score
        score = validation_results["overall_score"]
        status = "✅ PASSED" if validation_results["passed"] else "❌ FAILED"
        report.append(f"Overall Score: {score:.1f}% {status}")
        report.append("")

        # Workflow compliance
        workflow = validation_results["workflow_compliance"]
        report.append("📋 WORKFLOW COMPLIANCE")
        report.append(
            f"Status: {'✅ Complete' if workflow['complete'] else '❌ Incomplete'}"
        )
        report.append(
            f"Found: {len(workflow['found'])}/{len(self.workflow_steps)} steps"
        )
        if workflow["missing"]:
            report.append(f"Missing: {', '.join(workflow['missing'])}")
        report.append("")

        # BMAD enhancement compliance
        bmad = validation_results["bmad_enhancement_compliance"]
        report.append("🚀 BMAD ENHANCEMENT COMPLIANCE")
        report.append(
            f"Status: {'✅ Complete' if bmad['complete'] else '❌ Incomplete'}"
        )
        report.append(
            f"Found: {len(bmad['found'])}/{len(self.bmad_enhanced_steps)} enhancements"
        )
        if bmad["missing"]:
            report.append(f"Missing: {', '.join(bmad['missing'])}")
        report.append("")

        # Documentation references
        docs = validation_results["documentation_references"]
        report.append("📚 DOCUMENTATION REFERENCES")
        report.append(
            f"Status: {'✅ Complete' if docs['complete'] else '❌ Incomplete'}"
        )
        report.append(
            f"Referenced: {len(docs['found'])}/{len(self.required_docs)} files"
        )
        if docs["missing"]:
            report.append(f"Missing: {', '.join(docs['missing'])}")
        report.append("")

        # Rule compliance
        rules = validation_results["rule_compliance"]
        report.append("🔒 RULE COMPLIANCE")
        report.append(f"Score: {rules['score']:.1f}%")
        report.append(
            f"ALWAYS Rules Found: {rules['always_rules_found']}/{len(self.critical_rules['ALWAYS'])}"
        )
        if rules["violations"]:
            report.append(f"Violations: {len(rules['violations'])}")
            for violation in rules["violations"]:
                report.append(f"  - {violation}")
        report.append("")

        # Advanced elicitation compliance
        elicitation = validation_results["advanced_elicitation_compliance"]
        report.append("💡 ADVANCED ELICITATION COMPLIANCE")
        report.append(f"Score: {elicitation['score']:.1f}%")
        report.append(
            f"Methods Found: {len(elicitation['found'])}/{len(self.bmad_advanced_elicitation_methods)}"
        )
        if elicitation["found"]:
            report.append(
                f"Found Methods: {', '.join(elicitation['found'][:5])}{'...' if len(elicitation['found']) > 5 else ''}"
            )
        report.append("")

        # Business value documentation
        business_value = validation_results["business_value_documentation"]
        report.append("💼 BUSINESS VALUE DOCUMENTATION")
        report.append(f"Score: {business_value['score']:.1f}%")
        report.append(
            f"Status: {'✅ Complete' if business_value['complete'] else '❌ Incomplete'}"
        )
        report.append("")

        # Knowledge transfer documentation
        knowledge_transfer = validation_results["knowledge_transfer_documentation"]
        report.append("🧠 KNOWLEDGE TRANSFER DOCUMENTATION")
        report.append(f"Score: {knowledge_transfer['score']:.1f}%")
        report.append(
            f"Status: {'✅ Complete' if knowledge_transfer['complete'] else '❌ Incomplete'}"
        )
        report.append("")

        # Recommendations
        if validation_results["recommendations"]:
            report.append("💡 RECOMMENDATIONS")
            for rec in validation_results["recommendations"]:
                report.append(f"• {rec}")
            report.append("")

        report.append("=" * 70)
        return "\n".join(report)


def main():
    """CLI interface for the validator."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate BMAD-enhanced Context Engineering workflow compliance"
    )
    parser.add_argument(
        "input", help="Input file containing agent response or '-' for stdin"
    )
    parser.add_argument("--output", "-o", help="Output file for validation report")
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    # Read input
    if args.input == "-":
        response_text = input("Paste the agent response: ")
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            response_text = f.read()

    # Validate
    validator = BMADContextEngineeringValidator()
    results = validator.validate_response(response_text)

    # Generate output
    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output = validator.generate_report(results)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Validation report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
