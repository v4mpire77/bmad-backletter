#!/usr/bin/env python3
"""
Context Engineering Automation Tool

This tool helps agents automatically follow the Context Engineering workflow
by checking documentation, generating context summaries, and providing
implementation guidance.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextEngineeringAutomation:
    """
    Automates the Context Engineering workflow for agents.
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
            "architecture": "docs/ARCHITECTURE.md"
        }
        
        # Context Engineering specific docs
        self.ce_docs = {
            "workflow": "docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md",
            "quick_ref": "docs/AGENT_CE_QUICK_REFERENCE.md",
            "enforcement": "docs/AGENT_CE_ENFORCEMENT.md",
            "system_prompt": "docs/AGENT_CE_SYSTEM_PROMPT.md"
        }
    
    def generate_context_summary(self, task_description: str) -> Dict[str, any]:
        """
        Generate a comprehensive context summary for a given task.
        
        Args:
            task_description: Description of the task to analyze
            
        Returns:
            Dict containing context summary and recommendations
        """
        logger.info(f"Generating context summary for task: {task_description}")
        
        # Analyze task type
        task_type = self._analyze_task_type(task_description)
        
        # Get relevant documentation
        relevant_docs = self._get_relevant_documentation(task_type)
        
        # Generate implementation guidance
        implementation_guide = self._generate_implementation_guide(task_type, task_description)
        
        # Create context summary
        context_summary = {
            "task_analysis": {
                "description": task_description,
                "type": task_type,
                "complexity": self._assess_complexity(task_description),
                "estimated_effort": self._estimate_effort(task_type, task_description)
            },
            "documentation_references": relevant_docs,
            "implementation_guide": implementation_guide,
            "quality_requirements": self._get_quality_requirements(task_type),
            "workflow_checklist": self._get_workflow_checklist(),
            "generated_at": datetime.now().isoformat()
        }
        
        return context_summary
    
    def _analyze_task_type(self, task_description: str) -> str:
        """Analyze the task description to determine the type."""
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ["frontend", "ui", "component", "react", "next.js"]):
            return "frontend"
        elif any(word in task_lower for word in ["backend", "api", "service", "database", "python"]):
            return "backend"
        elif any(word in task_lower for word in ["rag", "nlp", "ai", "ml", "model"]):
            return "ai_ml"
        elif any(word in task_lower for word in ["test", "testing", "coverage", "qa"]):
            return "testing"
        elif any(word in task_lower for word in ["documentation", "docs", "readme"]):
            return "documentation"
        elif any(word in task_lower for word in ["deployment", "docker", "ci/cd", "infrastructure"]):
            return "devops"
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
                    "purpose": self._get_doc_purpose(key)
                }
        
        # Add type-specific docs
        if task_type == "frontend":
            relevant_docs["ui_ux"]["priority"] = "HIGH"
            if self._file_exists("frontend/README.md"):
                relevant_docs["frontend_readme"] = {
                    "path": "frontend/README.md",
                    "required": False,
                    "priority": "MEDIUM"
                }
        
        elif task_type == "backend":
            if self._file_exists("backend/README.md"):
                relevant_docs["backend_readme"] = {
                    "path": "backend/README.md",
                    "required": False,
                    "priority": "MEDIUM"
                }
        
        elif task_type == "ai_ml":
            if self._file_exists("docs/RAG_INTEGRATION_PLAN.md"):
                relevant_docs["rag_plan"] = {
                    "path": "docs/RAG_INTEGRATION_PLAN.md",
                    "required": False,
                    "priority": "HIGH"
                }
        
        # Add Context Engineering docs
        for key, path in self.ce_docs.items():
            if self._file_exists(path):
                relevant_docs[f"ce_{key}"] = {
                    "path": path,
                    "required": True,
                    "priority": "HIGH",
                    "purpose": self._get_ce_doc_purpose(key)
                }
        
        return relevant_docs
    
    def _generate_implementation_guide(self, task_type: str, task_description: str) -> Dict[str, any]:
        """Generate implementation guidance based on task type."""
        guide = {
            "workflow_steps": [
                "1. Context Assessment - Review all relevant documentation",
                "2. Implementation Plan - Create detailed implementation plan",
                "3. Implementation - Follow established patterns and architecture",
                "4. Documentation - Update code and documentation concurrently",
                "5. Verification - Check against quality standards and checklist"
            ],
            "file_placement": self._get_file_placement_guidance(task_type),
            "naming_conventions": self._get_naming_conventions(task_type),
            "testing_requirements": self._get_testing_requirements(task_type),
            "code_quality": self._get_code_quality_standards(task_type)
        }
        
        return guide
    
    def _get_file_placement_guidance(self, task_type: str) -> Dict[str, str]:
        """Get guidance on where to place new files."""
        if task_type == "frontend":
            return {
                "components": "frontend/components/",
                "pages": "frontend/app/",
                "utilities": "frontend/lib/",
                "styles": "frontend/app/globals.css or component-specific CSS modules",
                "types": "frontend/src/types/ or frontend/lib/types/"
            }
        elif task_type == "backend":
            return {
                "services": "backend/app/services/",
                "routers": "backend/app/routers/",
                "models": "backend/app/models/",
                "core": "backend/app/core/",
                "tests": "backend/tests/ or backend/app/tests/"
            }
        else:
            return {
                "general": "Follow project structure in docs/project_structure.md",
                "documentation": "docs/",
                "scripts": "scripts/ or tools/"
            }
    
    def _get_naming_conventions(self, task_type: str) -> Dict[str, str]:
        """Get naming conventions for the task type."""
        if task_type == "frontend":
            return {
                "components": "PascalCase (e.g., DocumentUpload.tsx)",
                "files": "kebab-case (e.g., document-upload.tsx)",
                "functions": "camelCase (e.g., handleFileUpload)",
                "constants": "UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)",
                "types": "PascalCase with descriptive names (e.g., UploadResponse)"
            }
        elif task_type == "backend":
            return {
                "modules": "snake_case (e.g., document_analyzer.py)",
                "classes": "PascalCase (e.g., DocumentAnalyzer)",
                "functions": "snake_case (e.g., analyze_document)",
                "variables": "snake_case (e.g., max_file_size)",
                "constants": "UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)"
            }
        else:
            return {
                "general": "Follow language-specific conventions",
                "files": "Use descriptive, lowercase names with appropriate separators"
            }
    
    def _get_testing_requirements(self, task_type: str) -> Dict[str, str]:
        """Get testing requirements for the task type."""
        base_requirements = {
            "coverage": "80%+ for new code",
            "unit_tests": "Required for all functions and methods",
            "integration_tests": "Required for API endpoints and workflows",
            "edge_cases": "Test error conditions and boundary cases"
        }
        
        if task_type == "frontend":
            base_requirements.update({
                "component_tests": "Test component rendering and interactions",
                "accessibility": "Ensure WCAG 2.1 AA compliance",
                "responsive": "Test on multiple screen sizes"
            })
        elif task_type == "backend":
            base_requirements.update({
                "api_tests": "Test all endpoints with various inputs",
                "database_tests": "Test database operations and migrations",
                "security": "Test authentication and authorization"
            })
        
        return base_requirements
    
    def _get_code_quality_standards(self, task_type: str) -> Dict[str, str]:
        """Get code quality standards for the task type."""
        standards = {
            "documentation": "Include docstrings and comments for complex logic",
            "error_handling": "Implement proper error handling and logging",
            "type_safety": "Use type hints where applicable",
            "formatting": "Follow language-specific formatting standards"
        }
        
        if task_type == "frontend":
            standards.update({
                "accessibility": "Include ARIA labels and semantic HTML",
                "performance": "Optimize bundle size and loading times",
                "responsive": "Ensure mobile-first design approach"
            })
        elif task_type == "backend":
            standards.update({
                "security": "Validate all inputs and implement proper authentication",
                "performance": "Use async operations and optimize database queries",
                "logging": "Implement comprehensive logging for debugging"
            })
        
        return standards
    
    def _get_quality_requirements(self, task_type: str) -> Dict[str, any]:
        """Get quality requirements for the task type."""
        return {
            "testing": {
                "coverage": "80%+",
                "types": ["unit", "integration", "edge_case"]
            },
            "documentation": {
                "code_docs": "Required",
                "api_docs": "Required for backend tasks",
                "user_docs": "Required for frontend tasks"
            },
            "performance": {
                "response_time": "< 2 seconds for API calls",
                "file_size": "< 10MB for uploads",
                "memory": "Efficient memory usage"
            },
            "security": {
                "input_validation": "Required",
                "authentication": "Required for protected endpoints",
                "data_encryption": "Required for sensitive data"
            }
        }
    
    def _get_workflow_checklist(self) -> List[str]:
        """Get the Context Engineering workflow checklist."""
        return [
            "✅ All relevant documentation reviewed",
            "✅ Implementation plan created",
            "✅ Code follows established patterns",
            "✅ Tests implemented and passing",
            "✅ Documentation updated",
            "✅ Code meets quality standards",
            "✅ No NEVER rules violated",
            "✅ All ALWAYS rules followed"
        ]
    
    def _assess_complexity(self, task_description: str) -> str:
        """Assess task complexity based on description."""
        task_lower = task_description.lower()
        
        # Simple indicators
        simple_indicators = ["add", "update", "fix", "modify", "change"]
        complex_indicators = ["implement", "create", "build", "develop", "integrate"]
        
        simple_count = sum(1 for indicator in simple_indicators if indicator in task_lower)
        complex_count = sum(1 for indicator in complex_indicators if indicator in task_lower)
        
        if complex_count > simple_count:
            return "HIGH"
        elif simple_count > complex_count:
            return "LOW"
        else:
            return "MEDIUM"
    
    def _estimate_effort(self, task_type: str, task_description: str) -> str:
        """Estimate effort required for the task."""
        complexity = self._assess_complexity(task_description)
        
        if complexity == "LOW":
            return "1-2 hours"
        elif complexity == "MEDIUM":
            return "4-8 hours"
        else:
            return "1-3 days"
    
    def _get_doc_purpose(self, doc_key: str) -> str:
        """Get the purpose of a documentation file."""
        purposes = {
            "implementation": "Overall project plan and implementation stages",
            "project_structure": "File organization and architecture guidelines",
            "ui_ux": "Design system and accessibility standards",
            "bug_tracking": "Known issues and resolution workflows",
            "architecture": "System architecture and technical design"
        }
        return purposes.get(doc_key, "Project documentation")
    
    def _get_ce_doc_purpose(self, doc_key: str) -> str:
        """Get the purpose of a Context Engineering documentation file."""
        purposes = {
            "workflow": "Mandatory workflow sequence for all tasks",
            "quick_ref": "Quick reference for Context Engineering workflow",
            "enforcement": "How to enforce the Context Engineering workflow",
            "system_prompt": "System prompt template for AI agents"
        }
        return purposes.get(doc_key, "Context Engineering guidance")
    
    def _file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        return (self.project_root / file_path).exists()
    
    def generate_workflow_template(self, task_description: str) -> str:
        """
        Generate a Context Engineering workflow template for the task.
        
        Args:
            task_description: Description of the task
            
        Returns:
            Formatted workflow template
        """
        context_summary = self.generate_context_summary(task_description)
        
        template = f"""
# Context Engineering Workflow Template

## Task: {task_description}

## 1. Context Assessment

### Required Documentation Review:
"""
        
        for doc_key, doc_info in context_summary["documentation_references"].items():
            if doc_info.get("required", False):
                template += f"- **{doc_info['path']}** - {doc_info.get('purpose', 'Required documentation')}\n"
        
        template += f"""

### Task Analysis:
- **Type:** {context_summary['task_analysis']['type']}
- **Complexity:** {context_summary['task_analysis']['complexity']}
- **Estimated Effort:** {context_summary['task_analysis']['estimated_effort']}

## 2. Implementation Plan

[Your implementation plan goes here]

## 3. Implementation

[Your implementation code goes here]

## 4. Documentation

[Documentation updates go here]

## 5. Verification against Checklist

{chr(10).join(context_summary['workflow_checklist'])}

## Quality Requirements

### Testing:
- Coverage: {context_summary['quality_requirements']['testing']['coverage']}
- Test Types: {', '.join(context_summary['quality_requirements']['testing']['types'])}

### Performance:
- API Response Time: {context_summary['quality_requirements']['performance']['response_time']}
- File Size Limit: {context_summary['quality_requirements']['performance']['file_size']}

### Security:
- Input Validation: {context_summary['quality_requirements']['security']['input_validation']}
- Authentication: {context_summary['quality_requirements']['security']['authentication']}
"""
        
        return template
    
    def save_context_summary(self, context_summary: Dict[str, any], output_path: str = None) -> str:
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
            output_path = f"context_summary_{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(context_summary, f, indent=2, default=str)
        
        logger.info(f"Context summary saved to {output_path}")
        return output_path

def main():
    """CLI interface for the automation tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Context Engineering Automation Tool")
    parser.add_argument("task", help="Description of the task to analyze")
    parser.add_argument("--output", "-o", help="Output file for context summary")
    parser.add_argument("--template", "-t", action="store_true", help="Generate workflow template")
    parser.add_argument("--project-root", "-p", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    # Initialize automation tool
    automation = ContextEngineeringAutomation(args.project_root)
    
    if args.template:
        # Generate workflow template
        template = automation.generate_workflow_template(args.task)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"Workflow template saved to {args.output}")
        else:
            print(template)
    else:
        # Generate context summary
        context_summary = automation.generate_context_summary(args.task)
        
        if args.output:
            output_path = automation.save_context_summary(context_summary, args.output)
            print(f"Context summary saved to {output_path}")
        else:
            print(json.dumps(context_summary, indent=2, default=str))

if __name__ == "__main__":
    main()
