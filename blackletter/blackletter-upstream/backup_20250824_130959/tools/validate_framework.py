"""
Framework Validation Tool

Validates codebase compliance with Context Engineering Framework standards.
"""

import os
import ast
import re
from typing import Dict, List, Tuple
import logging
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ValidationResult:
    """Results of framework validation."""
    total_files: int
    files_with_issues: int
    total_issues: int
    issues_by_type: Dict[str, int]
    detailed_issues: List[Dict[str, str]]

class FrameworkValidator:
    """Validates codebase against framework standards."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def validate_python_file(self, file_path: str) -> List[Dict[str, str]]:
        """Validate a Python file for framework compliance."""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            tree = ast.parse(content)
            
            # Check docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if not ast.get_docstring(node):
                        issues.append({
                            'type': 'missing_docstring',
                            'location': f'Line {node.lineno}',
                            'message': f'Missing docstring for {node.__class__.__name__}'
                        })
            
            # Check type hints
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.returns and not any(isinstance(d, ast.AnnAssign) for d in node.body):
                        issues.append({
                            'type': 'missing_type_hints',
                            'location': f'Line {node.lineno}',
                            'message': f'Missing return type hint for function {node.name}'
                        })
            
            # Check error handling
            try_count = len([n for n in ast.walk(tree) if isinstance(n, ast.Try)])
            if try_count == 0 and len(content.split('\n')) > 50:
                issues.append({
                    'type': 'missing_error_handling',
                    'location': 'File level',
                    'message': 'No error handling found in substantial file'
                })
            
            # Check performance monitoring
            if 'performance' not in content.lower() and len(content.split('\n')) > 100:
                issues.append({
                    'type': 'missing_performance_monitoring',
                    'location': 'File level',
                    'message': 'No performance monitoring found in substantial file'
                })
                
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'location': f'Line {e.lineno}',
                'message': str(e)
            })
            
        return issues
    
    def validate_typescript_file(self, file_path: str) -> List[Dict[str, str]]:
        """Validate a TypeScript file for framework compliance."""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check interfaces/types
        if not re.search(r'interface\s+\w+|type\s+\w+\s*=', content):
            issues.append({
                'type': 'missing_types',
                'location': 'File level',
                'message': 'No TypeScript interfaces or types defined'
            })
        
        # Check error handling
        if 'try' not in content and 'catch' not in content and len(content.split('\n')) > 50:
            issues.append({
                'type': 'missing_error_handling',
                'location': 'File level',
                'message': 'No error handling found in substantial file'
            })
        
        # Check performance monitoring
        if 'performance' not in content.lower() and len(content.split('\n')) > 100:
            issues.append({
                'type': 'missing_performance_monitoring',
                'location': 'File level',
                'message': 'No performance monitoring found in substantial file'
            })
        
        # Check documentation
        if not re.search(r'/\*\*[\s\S]*?\*/', content):
            issues.append({
                'type': 'missing_documentation',
                'location': 'File level',
                'message': 'No JSDoc documentation found'
            })
            
        return issues
    
    def validate_directory(self, directory: str) -> ValidationResult:
        """Validate all files in a directory for framework compliance."""
        total_files = 0
        files_with_issues = 0
        total_issues = 0
        issues_by_type = {}
        detailed_issues = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.ts', '.tsx')) and 'node_modules' not in root:
                    file_path = os.path.join(root, file)
                    total_files += 1
                    
                    # Validate file based on type
                    if file.endswith('.py'):
                        issues = self.validate_python_file(file_path)
                    else:
                        issues = self.validate_typescript_file(file_path)
                    
                    if issues:
                        files_with_issues += 1
                        total_issues += len(issues)
                        
                        # Update issue type counts
                        for issue in issues:
                            issue_type = issue['type']
                            issues_by_type[issue_type] = issues_by_type.get(issue_type, 0) + 1
                            
                        # Add detailed issues
                        for issue in issues:
                            detailed_issues.append({
                                'file': file_path,
                                'type': issue['type'],
                                'location': issue['location'],
                                'message': issue['message']
                            })
        
        return ValidationResult(
            total_files=total_files,
            files_with_issues=files_with_issues,
            total_issues=total_issues,
            issues_by_type=issues_by_type,
            detailed_issues=detailed_issues
        )

def main():
    """Run framework validation on the codebase."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    validator = FrameworkValidator()
    
    # Get project root (assumes script is in tools/ directory)
    project_root = str(Path(__file__).parent.parent)
    
    # Validate backend
    logger.info("Validating backend code...")
    backend_result = validator.validate_directory(os.path.join(project_root, 'backend'))
    
    # Validate frontend
    logger.info("Validating frontend code...")
    frontend_result = validator.validate_directory(os.path.join(project_root, 'frontend'))
    
    # Combine results
    total_files = backend_result.total_files + frontend_result.total_files
    total_issues = backend_result.total_issues + frontend_result.total_issues
    
    # Print summary
    print("\nFramework Validation Results")
    print("===========================")
    print(f"Total files checked: {total_files}")
    print(f"Files with issues: {backend_result.files_with_issues + frontend_result.files_with_issues}")
    print(f"Total issues found: {total_issues}")
    
    # Print issues by type
    print("\nIssues by Type")
    print("==============")
    all_types = set(backend_result.issues_by_type.keys()) | set(frontend_result.issues_by_type.keys())
    for issue_type in sorted(all_types):
        backend_count = backend_result.issues_by_type.get(issue_type, 0)
        frontend_count = frontend_result.issues_by_type.get(issue_type, 0)
        print(f"{issue_type}: {backend_count + frontend_count}")
    
    # Print detailed issues if any
    if total_issues > 0:
        print("\nDetailed Issues")
        print("===============")
        all_issues = backend_result.detailed_issues + frontend_result.detailed_issues
        for issue in all_issues:
            print(f"\nFile: {issue['file']}")
            print(f"Type: {issue['type']}")
            print(f"Location: {issue['location']}")
            print(f"Message: {issue['message']}")

if __name__ == '__main__':
    main()
