"""
Contract review service for Blackletter Systems.

This module provides functionality for reviewing contracts:
- Extract text from contracts
- Detect clauses and issues
- Generate summaries and redlines
"""

import os
import json
import re
from typing import Dict, List, Optional, Any
import logging
import yaml

from app.core.ocr import extract_text, extract_text_with_locations, detect_clauses
from app.core.storage import download_file, upload_file
from app.core.redact import create_redlined_document, create_summary_markdown
from app.core.llm_adapter import generate
from app.models.schemas import DocumentType, IssueSeverity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default clause patterns
DEFAULT_CLAUSE_PATTERNS = {
    "termination": [
        r"terminat(e|ion|ing)",
        r"cancel(lation)?",
        r"end(ing)? (of|the) (agreement|contract)"
    ],
    "assignment": [
        r"assign(ment)?",
        r"transfer of (rights|obligations)",
        r"novation"
    ],
    "liability": [
        r"liab(le|ility)",
        r"indemnif(y|ication)",
        r"hold harmless"
    ],
    "confidentiality": [
        r"confidential(ity)?",
        r"non-disclosure",
        r"proprietary information"
    ],
    "governing_law": [
        r"govern(ing)? law",
        r"jurisdiction",
        r"applicable law"
    ],
    "payment": [
        r"payment( terms)?",
        r"compensation",
        r"fee(s)?"
    ],
    "data_protection": [
        r"data protection",
        r"GDPR",
        r"personal (data|information)",
        r"privacy"
    ]
}

async def load_playbook(playbook_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Load a playbook for contract review.
    
    Args:
        playbook_name: Name of the playbook to load
        
    Returns:
        Dict[str, Any]: The playbook configuration
    """
    # Default playbook path
    if not playbook_name:
        playbook_name = "default"
    
    # Try to load from rules directory
    playbook_path = f"rules/{playbook_name}.yaml"
    
    try:
        with open(playbook_path, "r") as f:
            playbook = yaml.safe_load(f)
        
        logger.info(f"Loaded playbook from {playbook_path}")
        return playbook
    
    except FileNotFoundError:
        logger.warning(f"Playbook {playbook_path} not found, using default rules")
        
        # Return a default playbook
        return {
            "name": "Default Playbook",
            "description": "Default contract review rules",
            "version": "1.0",
            "clause_patterns": DEFAULT_CLAUSE_PATTERNS,
            "rules": [
                {
                    "id": "vague_terms",
                    "name": "Vague Terms",
                    "description": "Check for vague or ambiguous terms",
                    "patterns": [
                        r"reasonable",
                        r"best efforts",
                        r"commercially reasonable",
                        r"material",
                        r"substantial(ly)?",
                        r"as soon as practicable",
                        r"as necessary"
                    ],
                    "severity": "medium"
                },
                {
                    "id": "missing_definitions",
                    "name": "Missing Definitions",
                    "description": "Check for capitalized terms without definitions",
                    "patterns": [
                        r"[A-Z][a-z]+ [A-Z][a-z]+"
                    ],
                    "severity": "low"
                },
                {
                    "id": "gdpr_compliance",
                    "name": "GDPR Compliance",
                    "description": "Check for GDPR compliance issues",
                    "patterns": [
                        r"data protection",
                        r"personal data",
                        r"data subject",
                        r"data controller",
                        r"data processor"
                    ],
                    "severity": "high"
                }
            ]
        }

async def review_contract(
    document_key: str,
    document_type: DocumentType = DocumentType.CONTRACT,
    playbook: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Review a contract document.
    
    Args:
        document_key: S3 key of the document
        document_type: Type of document
        playbook: Name of the playbook to use
        metadata: Additional metadata
        
    Returns:
        Dict[str, Any]: Review results
    """
    try:
        # Download the document
        document_bytes = await download_file(document_key)
        
        # Extract text from the document
        logger.info(f"Extracting text from document {document_key}")
        text = extract_text(document_bytes)
        
        # Extract text with locations
        text_spans = extract_text_with_locations(document_bytes)
        
        # Load the playbook
        playbook_config = await load_playbook(playbook)
        
        # Detect clauses
        logger.info("Detecting clauses")
        clause_patterns = playbook_config.get("clause_patterns", DEFAULT_CLAUSE_PATTERNS)
        clauses = detect_clauses(text_spans, clause_patterns)
        
        # Detect issues based on rules
        logger.info("Detecting issues")
        issues = await detect_issues(text, playbook_config.get("rules", []))
        
        # Generate summary using LLM
        logger.info("Generating summary")
        summary = await generate_contract_summary(text, clauses, issues)
        
        # Create review JSON
        review = {
            "document_key": document_key,
            "document_type": document_type.value,
            "clauses": {
                clause_type: [
                    {
                        "text": span.text,
                        "page": span.page_num,
                        "bbox": span.bbox
                    }
                    for span in spans
                ]
                for clause_type, spans in clauses.items()
            },
            "issues": issues,
            "metadata": metadata or {}
        }
        
        # Count issues by severity
        issues_count = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for issue in issues:
            severity = issue.get("severity", "medium").lower()
            if severity in issues_count:
                issues_count[severity] += 1
        
        # Create markdown summary
        markdown_summary = create_summary_markdown(issues)
        
        # Create redlined document
        redlined_doc = create_redlined_document(text, issues)
        
        # Save results to S3
        summary_key = f"results/{document_key.split('/')[-1]}_summary.md"
        review_key = f"results/{document_key.split('/')[-1]}_review.json"
        redlined_key = f"results/{document_key.split('/')[-1]}_redlined.docx"
        
        # Upload results
        await upload_file(
            markdown_summary.encode("utf-8"),
            f"{document_key.split('/')[-1]}_summary.md",
            folder="results",
            content_type="text/markdown"
        )
        
        await upload_file(
            json.dumps(review, indent=2).encode("utf-8"),
            f"{document_key.split('/')[-1]}_review.json",
            folder="results",
            content_type="application/json"
        )
        
        await upload_file(
            redlined_doc,
            f"{document_key.split('/')[-1]}_redlined.docx",
            folder="results",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        # Return results
        return {
            "document_key": document_key,
            "summary_key": summary_key,
            "review_key": review_key,
            "redlined_key": redlined_key,
            "issues_count": issues_count
        }
    
    except Exception as e:
        logger.error(f"Error reviewing contract: {str(e)}")
        raise

async def detect_issues(
    text: str,
    rules: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Detect issues in the contract based on rules.
    
    Args:
        text: The contract text
        rules: List of rules to check
        
    Returns:
        List[Dict[str, Any]]: List of detected issues
    """
    issues = []
    
    for rule in rules:
        patterns = rule.get("patterns", [])
        severity = rule.get("severity", "medium")
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Get some context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Create issue
                issue = {
                    "text": context,
                    "start": start,
                    "end": end,
                    "severity": severity,
                    "rule_id": rule.get("id"),
                    "rule_name": rule.get("name"),
                    "comment": rule.get("description")
                }
                
                issues.append(issue)
    
    # Use LLM to analyze issues and provide suggestions
    if issues:
        issues = await enhance_issues_with_llm(text, issues)
    
    return issues

async def enhance_issues_with_llm(
    text: str,
    issues: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Enhance issues with LLM-generated suggestions.
    
    Args:
        text: The contract text
        issues: List of detected issues
        
    Returns:
        List[Dict[str, Any]]: Enhanced issues with suggestions
    """
    # Prepare context for LLM
    context = "I have detected the following issues in a legal contract:\n\n"
    
    for i, issue in enumerate(issues, 1):
        context += f"Issue {i}:\n"
        context += f"Text: \"{issue['text']}\"\n"
        context += f"Rule: {issue['rule_name']}\n"
        context += f"Severity: {issue['severity']}\n\n"
    
    # Generate suggestions with LLM
    prompt = f"{context}\nFor each issue, provide a brief suggestion on how to improve or fix it. Format your response as a JSON array of objects with 'issue_number' and 'suggestion' fields."
    
    system_prompt = "You are a legal expert specialized in contract analysis. Provide clear, concise suggestions for improving problematic contract clauses."
    
    try:
        response = await generate(prompt, system_prompt)
        
        # Extract suggestions from response
        import json
        try:
            suggestions = json.loads(response)
            
            # Add suggestions to issues
            for suggestion in suggestions:
                issue_number = suggestion.get("issue_number")
                if 1 <= issue_number <= len(issues):
                    issues[issue_number - 1]["suggestion"] = suggestion.get("suggestion")
        
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM response as JSON")
            
            # Try to extract suggestions using regex
            pattern = r"Issue (\d+).*?Suggestion: (.*?)(?=Issue \d+|$)"
            matches = re.finditer(pattern, response, re.DOTALL)
            
            for match in matches:
                issue_number = int(match.group(1))
                suggestion = match.group(2).strip()
                
                if 1 <= issue_number <= len(issues):
                    issues[issue_number - 1]["suggestion"] = suggestion
    
    except Exception as e:
        logger.error(f"Error enhancing issues with LLM: {str(e)}")
    
    return issues

async def generate_contract_summary(
    text: str,
    clauses: Dict[str, List[Any]],
    issues: List[Dict[str, Any]]
) -> str:
    """
    Generate a summary of the contract using LLM.
    
    Args:
        text: The contract text
        clauses: Detected clauses
        issues: Detected issues
        
    Returns:
        str: Contract summary
    """
    # Prepare context for LLM
    context = "I need a summary of a legal contract. Here are some key details:\n\n"
    
    # Add information about clauses
    context += "Key clauses found:\n"
    for clause_type, spans in clauses.items():
        if spans:
            context += f"- {clause_type.replace('_', ' ').title()}: {len(spans)} instances\n"
    
    # Add information about issues
    context += "\nIssues found:\n"
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    
    for issue in issues:
        severity = issue.get("severity", "medium").lower()
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    for severity, count in severity_counts.items():
        if count > 0:
            context += f"- {severity.title()}: {count} issues\n"
    
    # Add the first part of the contract text
    max_chars = 3000  # Limit text to avoid token limits
    context += f"\nContract text (excerpt):\n{text[:max_chars]}...\n"
    
    # Generate summary with LLM
    prompt = f"{context}\nPlease provide a concise summary of this contract, highlighting key provisions and potential risks. Format your response as markdown."
    
    system_prompt = "You are a legal expert specialized in contract analysis. Provide clear, structured summaries of legal documents, highlighting key provisions and risks."
    
    try:
        summary = await generate(prompt, system_prompt)
        return summary
    
    except Exception as e:
        logger.error(f"Error generating contract summary: {str(e)}")
        return "Failed to generate summary."
