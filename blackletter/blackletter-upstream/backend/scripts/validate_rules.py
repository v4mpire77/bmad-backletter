#!/usr/bin/env python3
"""
Validate GDPR rules configuration.

Usage:
    python validate_rules.py [path/to/rules.json]
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rules_validator import validate_rules_file

def main():
    rules_path = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        validate_rules_file(rules_path)
        print("✅ Rules validation passed")
        return 0
    except ValueError as e:
        print(f"❌ Rules validation failed:\n{e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
