import json
import re
from typing import List
from ..models import rules as m

def load_rules(path: str) -> m.RuleSet:
    """
    Load and validate GDPR rules from JSON file.
    
    Args:
        path: Path to the GDPR rules JSON file
        
    Returns:
        Validated RuleSet object
        
    Raises:
        ValueError: If rules are invalid or contain bad regex patterns
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Parse with Pydantic validation
    rs = m.RuleSet(**data)
    errors: List[str] = []

    # Additional validation for regex patterns
    for rule in rs.rules:
        for check in rule.checks:
            if hasattr(check, "patterns"):
                for p in getattr(check, "patterns"):
                    try:
                        re.compile(p)
                    except re.error as e:
                        errors.append(f"{rule.id} invalid regex '{p}': {e}")
            if check.type == "negation_regex":
                try:
                    re.compile(check.pattern)  # type: ignore
                except re.error as e:
                    errors.append(f"{rule.id} invalid negation_regex '{check.pattern}': {e}")
    
    if errors:
        raise ValueError("\n".join(errors))
    
    return rs

def validate_rules_file(path: str) -> bool:
    """
    Validate rules file without loading into memory.
    
    Args:
        path: Path to rules file
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    try:
        load_rules(path)
        return True
    except Exception as e:
        raise ValueError(f"Rules validation failed: {e}")

# Usage example for CLI validation:
# python -c "from app.services.rules_validator import load_rules; load_rules('rules/gdpr_rules.json'); print('Rules OK')"