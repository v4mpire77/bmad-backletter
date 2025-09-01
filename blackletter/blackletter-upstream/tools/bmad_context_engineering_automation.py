#!/usr/bin/env python3
"""
BMAD-Enhanced Context Engineering Automation Tool

This tool helps agents automatically follow the Context Engineering workflow
with BMAD (Business Model Analysis and Design) enhancements, including advanced
elicitation techniques, business context assessment, and risk management.
"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BMADContextEngineeringAutomation:
    """
    Automates the BMAD-Enhanced Context Engineering workflow for agents.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.docs_path = self.project_root / "docs"
        self.rules_path = self.project_root / "rules"
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"

        # Core documentation files
        self.core_docs = {
            "implementation": "docs/Implementation.md",
            "project_structure": "docs/project_structure.md",
            "ui_ux": "docs/UI_UX_doc.md",
            "bug_tracking": "docs/Bug_tracking.md",
            "architecture": "docs/ARCHITECTURE.md",
            "business_requirements": "docs/Business_Requirements.md",
            "business_value": "docs/Business_Value_Assessment.md",
        }

        # Context Engineering specific docs
        self.ce_docs = {
            "workflow": "docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md",
            "quick_ref": "docs/AGENT_CE_QUICK_REFERENCE.md",
            "enforcement": "docs/AGENT_CE_ENFORCEMENT.md",
            "system_prompt": "docs/AGENT_CE_SYSTEM_PROMPT.md",
        }

        # BMAD-specific documentation
        self.bmad_docs = {
            "bmad_method": "BMAD-METHOD-main/dist/agents/bmad-master.txt",
            "advanced_elicitation": "docs/BMAD_ADVANCED_ELICITATION_GUIDELINES.md",
        }

    def generate_context_summary(self, task_description: str) -> Dict[str, any]:
        """
        Generate a comprehensive BMAD-enhanced context summary for a given task.

        Args:
            task_description: Description of the task to analyze

        Returns:
            Dict containing context summary and recommendations
        """
        logger.info(
            f"Generating BMAD-enhanced context summary for task: {task_description}"
        )

        # Analyze task type
        task_type = self._analyze_task_type(task_description)

        # Get relevant documentation
        relevant_docs = self._get_relevant_documentation(task_type)

        # Generate implementation guidance
        implementation_guide = self._generate_implementation_guide(
            task_type, task_description
        )

        # Generate BMAD business context assessment
        business_context = self._generate_business_context_assessment(task_description)

        # Generate BMAD risk assessment
        risk_assessment = self._generate_risk_assessment(task_description)

        # Generate advanced elicitation options
        elicitation_options = self._generate_elicitation_options(
            task_description, task_type
        )

        # Create context summary
        context_summary = {
            "task_analysis": {
                "description": task_description,
                "type": task_type,
                "complexity": self._assess_complexity(task_description),
                "estimated_effort": self._estimate_effort(task_type, task_description),
                "business_impact": business_context["impact_level"],
            },
            "documentation_references": relevant_docs,
            "implementation_guide": implementation_guide,
            "business_context_assessment": business_context,
            "risk_assessment": risk_assessment,
            "advanced_elicitation": elicitation_options,
            "quality_requirements": self._get_quality_requirements(task_type),
            "workflow_checklist": self._get_workflow_checklist(),
            "generated_at": datetime.now().isoformat(),
        }

        return context_summary

    def _analyze_task_type(self, task_description: str) -> str:
        """Analyze the task description to determine the type."""
        task_lower = task_description.lower()

        if any(
            word in task_lower
            for word in ["frontend", "ui", "component", "react", "next.js"]
        ):
            return "frontend"
        elif any(
            word in task_lower
            for word in ["backend", "api", "service", "database", "python"]
        ):
            return "backend"
        elif any(word in task_lower for word in ["rag", "nlp", "ai", "ml", "model"]):
            return "ai_ml"
        elif any(word in task_lower for word in ["test", "testing", "coverage", "qa"]):
            return "testing"
        elif any(word in task_lower for word in ["documentation", "docs", "readme"]):
            return "documentation"
        elif any(
            word in task_lower
            for word in ["deployment", "docker", "ci/cd", "infrastructure"]
        ):
            return "devops"
        elif any(
            word in task_lower
            for word in ["business", "value", "stakeholder", "requirement"]
        ):
            return "business_analysis"
        else:
            return "general"

    def _get_relevant_documentation(self, task_type: str) -> Dict[str, any]:
        """Get relevant documentation based on task type."""
        relevant_docs = {}

        # Always include core docs
        for key, path in self.core_docs.items():
            if self._file_exists(path):
                relevant_docs[key] = {
                    "path": path,
                    "required": True,
                    "purpose": self._get_doc_purpose(key),
                }

        # Add type-specific docs
        if task_type == "frontend":
            relevant_docs["ui_ux"]["priority"] = "HIGH"
            if self._file_exists("frontend/README.md"):
                relevant_docs["frontend_readme"] = {
                    "path": "frontend/README.md",
                    "required": False,
                    "priority": "MEDIUM",
                }

        elif task_type == "backend":
            if self._file_exists("backend/README.md"):
                relevant_docs["backend_readme"] = {
                    "path": "backend/README.md",
                    "required": False,
                    "priority": "MEDIUM",
                }

        elif task_type == "ai_ml":
            if self._file_exists("docs/RAG_INTEGRATION_PLAN.md"):
                relevant_docs["rag_plan"] = {
                    "path": "docs/RAG_INTEGRATION_PLAN.md",
                    "required": False,
                    "priority": "HIGH",
                }

        # Add Context Engineering docs
        for key, path in self.ce_docs.items():
            if self._file_exists(path):
                relevant_docs[f"ce_{key}"] = {
                    "path": path,
                    "required": True,
                    "priority": "HIGH",
                    "purpose": self._get_ce_doc_purpose(key),
                }

        # Add BMAD docs
        for key, path in self.bmad_docs.items():
            if self._file_exists(path):
                relevant_docs[f"bmad_{key}"] = {
                    "path": path,
                    "required": True,
                    "priority": "HIGH",
                    "purpose": self._get_bmad_doc_purpose(key),
                }

        return relevant_docs

    def _generate_implementation_guide(
        self, task_type: str, task_description: str
    ) -> Dict[str, any]:
        """Generate implementation guidance based on task type."""
        guide = {
            "workflow_steps": [
                "1. Business Context Assessment - Review business requirements and value",
                "2. Technical Context Assessment - Review all relevant documentation",
                "3. Risk and Compatibility Analysis - Identify risks and compatibility requirements",
                "4. Implementation Plan - Create detailed implementation plan",
                "5. Implementation - Follow established patterns and architecture",
                "6. Advanced Elicitation - Apply BMAD techniques for deeper exploration",
                "7. Documentation - Update code and documentation concurrently",
                "8. Verification - Check against quality standards and checklist",
            ],
            "file_placement": self._get_file_placement_guidance(task_type),
            "naming_conventions": self._get_naming_conventions(task_type),
            "testing_requirements": self._get_testing_requirements(task_type),
            "code_quality": self._get_code_quality_standards(task_type),
        }

        return guide

    def _generate_business_context_assessment(
        self, task_description: str
    ) -> Dict[str, any]:
        """Generate BMAD business context assessment."""
        return {
            "stakeholder_needs": "Analyze business requirements document (docs/Business_Requirements.md)",
            "value_proposition": "Review business value assessment (docs/Business_Value_Assessment.md)",
            "success_metrics": "Identify key performance indicators and success criteria",
            "impact_level": self._assess_business_impact(task_description),
            "alignment_check": "Ensure technical implementation aligns with business objectives",
        }

    def _generate_risk_assessment(self, task_description: str) -> Dict[str, any]:
        """Generate BMAD risk assessment."""
        return {
            "technical_risks": [
                "Assess potential impact on existing functionality",
                "Identify integration complexity",
                "Determine rollback requirements",
            ],
            "business_risks": [
                "Evaluate impact on business operations",
                "Identify stakeholder dependencies",
                "Assess timeline implications",
            ],
            "mitigation_strategies": [
                "Document rollback procedures",
                "Plan for incremental deployment",
                "Establish monitoring and alerting",
            ],
        }

    def _generate_elicitation_options(
        self, task_description: str, task_type: str
    ) -> Dict[str, any]:
        """Generate BMAD advanced elicitation options."""
        # Core methods (always include)
        core_methods = [
            "Expand or Contract for Audience",
            "Critique and Refine",
            "Identify Potential Risks",
            "Assess Alignment with Goals",
        ]

        # Context-specific methods
        context_methods = []
        if task_type in ["backend", "ai_ml"]:
            context_methods.extend(["Tree of Thoughts", "ReWOO", "Meta-Prompting"])
        elif task_type in ["frontend", "ui_ux"]:
            context_methods.extend(["Agile Team Perspective", "Stakeholder Roundtable"])
        elif task_type == "business_analysis":
            context_methods.extend(
                [
                    "Innovation Tournament",
                    "Escape Room Challenge",
                    "Red Team vs Blue Team",
                    "Hindsight Reflection",
                ]
            )
        else:
            context_methods.extend(["Agile Team Perspective", "Stakeholder Roundtable"])

        # Combine methods (limit to 9)
        elicitation_methods = (core_methods + context_methods)[:9]

        return {
            "methods": elicitation_methods,
            "when_to_apply": "After drafting significant sections of code, documentation, or design",
            "process": "Present 9 intelligently selected methods plus 'Proceed' option",
            "execution": "Execute selected method and provide actionable insights",
        }

    def _get_file_placement_guidance(self, task_type: str) -> Dict[str, str]:
        """Get guidance on where to place new files."""
        if task_type == "frontend":
            return {
                "components": "frontend/components/",
                "pages": "frontend/app/",
                "utilities": "frontend/lib/",
                "styles": "frontend/app/globals.css or component-specific CSS modules",
                "types": "frontend/src/types/ or frontend/lib/types/",
            }
        elif task_type == "backend":
            return {
                "services": "backend/app/services/",
                "routers": "backend/app/routers/",
                "models": "backend/app/models/",
                "core": "backend/app/core/",
                "tests": "backend/tests/ or backend/app/tests/",
            }
        else:
            return {
                "general": "Follow project structure in docs/project_structure.md",
                "documentation": "docs/",
                "scripts": "scripts/ or tools/",
            }

    def _get_naming_conventions(self, task_type: str) -> Dict[str, str]:
        """Get naming conventions for the task type."""
        if task_type == "frontend":
            return {
                "components": "PascalCase (e.g., DocumentUpload.tsx)",
                "files": "kebab-case (e.g., document-upload.tsx)",
                "functions": "camelCase (e.g., handleFileUpload)",
                "constants": "UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)",
                "types": "PascalCase with descriptive names (e.g., UploadResponse)",
            }
        elif task_type == "backend":
            return {
                "modules": "snake_case (e.g., document_analyzer.py)",
                "classes": "PascalCase (e.g., DocumentAnalyzer)",
                "functions": "snake_case (e.g., analyze_document)",
                "variables": "snake_case (e.g., max_file_size)",
                "constants": "UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)",
            }
        else:
            return {
                "general": "Follow language-specific conventions",
                "files": "Use descriptive, lowercase names with appropriate separators",
            }

    def _get_testing_requirements(self, task_type: str) -> Dict[str, str]:
        """Get testing requirements for the task type."""
        base_requirements = {
            "coverage": "80%+ for new code",
            "types": ["unit", "integration", "edge_case", "business_scenario"],
        }

        if task_type == "frontend":
            base_requirements["types"].extend(
                ["component", "accessibility", "responsive"]
            )
        elif task_type == "backend":
            base_requirements["types"].extend(["api", "database", "security"])

        return base_requirements

    def _get_code_quality_standards(self, task_type: str) -> Dict[str, str]:
        """Get code quality standards for the task type."""
        standards = {
            "documentation": "Include docstrings and comments for complex logic",
            "error_handling": "Implement proper error handling and logging",
            "type_safety": "Use type hints where applicable",
            "formatting": "Follow language-specific formatting standards",
            "business_logic": "Document business logic and decision rationale",
        }

        if task_type == "frontend":
            standards.update(
                {
                    "accessibility": "Include ARIA labels and semantic HTML",
                    "performance": "Optimize bundle size and loading times",
                    "responsive": "Ensure mobile-first design approach",
                }
            )
        elif task_type == "backend":
            standards.update(
                {
                    "security": "Validate all inputs and implement proper authentication",
                    "performance": "Use async operations and optimize database queries",
                    "logging": "Implement comprehensive logging for debugging",
                }
            )

        return standards

    def _get_quality_requirements(self, task_type: str) -> Dict[str, any]:
        """Get quality requirements for the task type."""
        return {
            "testing": {
                "coverage": "80%+",
                "types": ["unit", "integration", "edge_case", "business_scenario"],
            },
            "documentation": {
                "code_docs": "Required with business context",
                "api_docs": "Required for backend tasks",
                "user_docs": "Required for frontend tasks",
                "business_docs": "Required for all tasks with business impact",
            },
            "performance": {
                "response_time": "< 2 seconds for API calls",
                "file_size": "< 10MB for uploads",
                "memory": "Efficient memory usage",
            },
            "security": {
                "input_validation": "Required",
                "authentication": "Required for protected endpoints",
                "data_encryption": "Required for sensitive data",
            },
            "business_value": {
                "alignment": "Implementation must align with business objectives",
                "documentation": "Document business value delivered by each component",
                "success_criteria": "Validate against business success criteria",
            },
        }

    def _get_workflow_checklist(self) -> List[str]:
        """Get the BMAD-Enhanced Context Engineering workflow checklist."""
        return [
            "✅ Business context and stakeholder needs analyzed",
            "✅ Business value and impact assessed",
            "✅ All relevant documentation reviewed",
            "✅ Code follows established project patterns",
            "✅ Tests implemented and passing",
            "✅ Documentation updated with business context",
            "✅ Code meets quality standards",
            "✅ Risks identified and mitigation strategies documented",
            "✅ No NEVER rules violated",
            "✅ All ALWAYS rules followed",
            "✅ Implementation validates against business success criteria",
            "✅ Business value delivered by implementation is documented",
            "✅ Advanced elicitation techniques applied where appropriate",
        ]

    def _assess_complexity(self, task_description: str) -> str:
        """Assess task complexity based on description."""
        task_lower = task_description.lower()

        # Simple indicators
        simple_indicators = ["add", "update", "fix", "modify", "change"]
        complex_indicators = ["implement", "create", "build", "develop", "integrate"]

        simple_count = sum(
            1 for indicator in simple_indicators if indicator in task_lower
        )
        complex_count = sum(
            1 for indicator in complex_indicators if indicator in task_lower
        )

        if complex_count > simple_count:
            return "HIGH"
        elif simple_count > complex_count:
            return "LOW"
        else:
            return "MEDIUM"

    def _assess_business_impact(self, task_description: str) -> str:
        """Assess business impact based on description."""
        task_lower = task_description.lower()

        # High impact indicators
        high_impact_indicators = [
            "revenue",
            "customer",
            "user experience",
            "compliance",
            "gdpr",
            "critical",
        ]
        # Medium impact indicators
        medium_impact_indicators = [
            "feature",
            "functionality",
            "improvement",
            "enhancement",
        ]
        # Low impact indicators
        low_impact_indicators = ["bug", "fix", "typo", "minor"]

        high_count = sum(
            1 for indicator in high_impact_indicators if indicator in task_lower
        )
        medium_count = sum(
            1 for indicator in medium_impact_indicators if indicator in task_lower
        )
        low_count = sum(
            1 for indicator in low_impact_indicators if indicator in task_lower
        )

        if high_count > medium_count and high_count > low_count:
            return "HIGH"
        elif low_count > high_count and low_count > medium_count:
            return "LOW"
        else:
            return "MEDIUM"

    def _estimate_effort(self, task_type: str, task_description: str) -> str:
        """Estimate effort required for the task."""
        complexity = self._assess_complexity(task_description)
        business_impact = self._assess_business_impact(task_description)

        if complexity == "HIGH" or business_impact == "HIGH":
            return "1-3 days"
        elif complexity == "MEDIUM" or business_impact == "MEDIUM":
            return "4-8 hours"
        else:
            return "1-2 hours"

    def _get_doc_purpose(self, doc_key: str) -> str:
        """Get the purpose of a documentation file."""
        purposes = {
            "implementation": "Overall project plan and implementation stages",
            "project_structure": "File organization and architecture guidelines",
            "ui_ux": "Design system and accessibility standards",
            "bug_tracking": "Known issues and resolution workflows",
            "architecture": "System architecture and technical design",
            "business_requirements": "Business value proposition and stakeholder needs",
            "business_value": "Business impact evaluation criteria and success metrics",
        }
        return purposes.get(doc_key, "Project documentation")

    def _get_ce_doc_purpose(self, doc_key: str) -> str:
        """Get the purpose of a Context Engineering documentation file."""
        purposes = {
            "workflow": "Mandatory workflow sequence for all tasks",
            "quick_ref": "Quick reference for Context Engineering workflow",
            "enforcement": "How to enforce the Context Engineering workflow",
            "system_prompt": "System prompt template for AI agents",
        }
        return purposes.get(doc_key, "Context Engineering guidance")

    def _get_bmad_doc_purpose(self, doc_key: str) -> str:
        """Get the purpose of a BMAD documentation file."""
        purposes = {
            "bmad_method": "BMAD method core principles and workflows",
            "advanced_elicitation": "Guidelines for BMAD advanced elicitation techniques",
        }
        return purposes.get(doc_key, "BMAD guidance")

    def _file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        return (self.project_root / file_path).exists()

    def generate_workflow_template(self, task_description: str) -> str:
        """
        Generate a BMAD-Enhanced Context Engineering workflow template for the task.

        Args:
            task_description: Description of the task

        Returns:
            Formatted workflow template
        """
        context_summary = self.generate_context_summary(task_description)

        template = f"""
# BMAD-Enhanced Context Engineering Workflow Template

## Task: {task_description}

## 1. Business Context Assessment

### Required Documentation Review:
- **docs/Business_Requirements.md** - Business value proposition and stakeholder needs
- **docs/Business_Value_Assessment.md** - Business impact evaluation criteria

### Business Analysis:
- **Stakeholder Needs:** {context_summary['business_context_assessment']['stakeholder_needs']}
- **Value Proposition:** {context_summary['business_context_assessment']['value_proposition']}
- **Success Metrics:** {context_summary['business_context_assessment']['success_metrics']}
- **Impact Level:** {context_summary['business_context_assessment']['impact_level']}

## 2. Technical Context Assessment

### Required Documentation Review:
"""

        for doc_key, doc_info in context_summary["documentation_references"].items():
            if doc_info.get("required", False) and "business" not in doc_key:
                template += f"- **{doc_info['path']}** - {doc_info.get('purpose', 'Required documentation')}\n"

        template += f"""

### Task Analysis:
- **Type:** {context_summary['task_analysis']['type']}
- **Complexity:** {context_summary['task_analysis']['complexity']}
- **Estimated Effort:** {context_summary['task_analysis']['estimated_effort']}

## 3. Risk and Compatibility Analysis

### Technical Risks:
"""
        for risk in context_summary["risk_assessment"]["technical_risks"]:
            template += f"- {risk}\n"

        template += "\n### Business Risks:\n"
        for risk in context_summary["risk_assessment"]["business_risks"]:
            template += f"- {risk}\n"

        template += "\n### Mitigation Strategies:\n"
        for strategy in context_summary["risk_assessment"]["mitigation_strategies"]:
            template += f"- {strategy}\n"

        template += f"""

## 4. Implementation Plan

[Your implementation plan goes here]

## 5. Implementation

[Your implementation code goes here]

## 6. Advanced Elicitation

### When to Apply:
{context_summary['advanced_elicitation']['when_to_apply']}

### Available Methods:
"""
        for i, method in enumerate(context_summary["advanced_elicitation"]["methods"]):
            template += f"{i}. {method}\n"

        template += """
9. Proceed / No Further Actions

[Apply advanced elicitation techniques as needed during implementation]

## 7. Documentation

[Documentation updates go here, including business context and value delivery]

## 8. Verification against Checklist

"""
        for item in context_summary["workflow_checklist"]:
            template += f"{item}\n"

        template += f"""

## Quality Requirements

### Testing:
- Coverage: {context_summary['quality_requirements']['testing']['coverage']}
- Test Types: {', '.join(context_summary['quality_requirements']['testing']['types'])}

### Business Value Documentation:
- Alignment: {context_summary['quality_requirements']['business_value']['alignment']}
- Documentation: {context_summary['quality_requirements']['business_value']['documentation']}
- Success Criteria: {context_summary['quality_requirements']['business_value']['success_criteria']}

### Performance:
- API Response Time: {context_summary['quality_requirements']['performance']['response_time']}
- File Size Limit: {context_summary['quality_requirements']['performance']['file_size']}

### Security:
- Input Validation: {context_summary['quality_requirements']['security']['input_validation']}
- Authentication: {context_summary['quality_requirements']['security']['authentication']}
"""

        return template

    def save_context_summary(
        self, context_summary: Dict[str, any], output_path: str = None
    ) -> str:
        """
        Save the context summary to a file.

        Args:
            context_summary: The context summary to save
            output_path: Path to save the file (optional)

        Returns:
            Path where the file was saved
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"bmad_context_summary_{timestamp}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(context_summary, f, indent=2, default=str)

        logger.info(f"BMAD-enhanced context summary saved to {output_path}")
        return output_path


def main():
    """CLI interface for the BMAD-enhanced automation tool."""
    import argparse

    parser = argparse.ArgumentParser(
        description="BMAD-Enhanced Context Engineering Automation Tool"
    )
    parser.add_argument("task", help="Description of the task to analyze")
    parser.add_argument("--output", "-o", help="Output file for context summary")
    parser.add_argument(
        "--template", "-t", action="store_true", help="Generate workflow template"
    )
    parser.add_argument(
        "--project-root", "-p", default=".", help="Project root directory"
    )

    args = parser.parse_args()

    # Initialize automation tool
    automation = BMADContextEngineeringAutomation(args.project_root)

    if args.template:
        # Generate workflow template
        template = automation.generate_workflow_template(args.task)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(template)
            print(f"BMAD-enhanced workflow template saved to {args.output}")
        else:
            print(template)
    else:
        # Generate context summary
        context_summary = automation.generate_context_summary(args.task)

        if args.output:
            output_path = automation.save_context_summary(context_summary, args.output)
            print(f"BMAD-enhanced context summary saved to {output_path}")
        else:
            print(json.dumps(context_summary, indent=2, default=str))


if __name__ == "__main__":
    main()
