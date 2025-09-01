# Context Engineering Tools

This directory contains tools and utilities to help agents follow the Context Engineering workflow and ensure compliance with the Blackletter Systems development standards.

## 🛠️ Available Tools

### 1. Context Engineering Validator (`context_engineering_validator.py`)

**Purpose:** Validates agent responses against the Context Engineering workflow requirements.

**Features:**
- Checks for required workflow steps
- Validates documentation references
- Ensures rule compliance
- Generates detailed validation reports
- Provides specific improvement recommendations

**Usage:**
```bash
# Validate from file
python tools/context_engineering_validator.py response.txt

# Validate from stdin
python tools/context_engineering_validator.py -

# Output to file
python tools/context_engineering_validator.py response.txt --output validation_report.txt

# JSON output
python tools/context_engineering_validator.py response.txt --json
```

**Output Example:**
```
============================================================
CONTEXT ENGINEERING WORKFLOW VALIDATION REPORT
============================================================

Overall Score: 85.0% ✅ PASSED

📋 WORKFLOW COMPLIANCE
Status: ✅ Complete
Found: 5/5 steps

📚 DOCUMENTATION REFERENCES
Status: ✅ Complete
Referenced: 4/4 files

🔒 RULE COMPLIANCE
Score: 90.0%
ALWAYS Rules Found: 7/8

💡 RECOMMENDATIONS
• Improve compliance with ALWAYS rules
• Ensure all critical requirements are addressed
============================================================
```

### 2. Context Engineering Automation (`context_engineering_automation.py`)

**Purpose:** Automates the Context Engineering workflow by generating context summaries and implementation guidance.

**Features:**
- Analyzes task complexity and type
- Identifies relevant documentation
- Generates implementation guidance
- Creates workflow templates
- Provides quality requirements

**Usage:**
```bash
# Generate context summary
python tools/context_engineering_automation.py "Implement user authentication"

# Generate workflow template
python tools/context_engineering_automation.py "Add file upload component" --template

# Save to file
python tools/context_engineering_automation.py "Create RAG endpoint" --output context.json

# Specify project root
python tools/context_engineering_automation.py "Update UI component" --project-root /path/to/project
```

**Output Example:**
```json
{
  "task_analysis": {
    "description": "Implement user authentication",
    "type": "backend",
    "complexity": "MEDIUM",
    "estimated_effort": "4-8 hours"
  },
  "documentation_references": {
    "implementation": {
      "path": "docs/Implementation.md",
      "required": true,
      "purpose": "Overall project plan and implementation stages"
    }
  },
  "implementation_guide": {
    "file_placement": {
      "services": "backend/app/services/",
      "routers": "backend/app/routers/"
    }
  }
}
```

### 3. PowerShell Script (`context_engineering.ps1`)

**Purpose:** Provides easy access to Context Engineering tools on Windows systems.

**Features:**
- Windows-native interface
- Color-coded output
- Easy command execution
- Built-in help and examples

**Usage:**
```powershell
# Show help
.\tools\context_engineering.ps1

# Generate context summary
.\tools\context_engineering.ps1 -Task "Implement user authentication" -Action summary

# Generate workflow template
.\tools\context_engineering.ps1 -Task "Add file upload component" -Action template

# Show workflow
.\tools\context_engineering.ps1 -Action workflow

# List documentation
.\tools\context_engineering.ps1 -Action docs
```

## 🔧 Installation and Setup

### Prerequisites

1. **Python 3.7+** - Required for Python tools
2. **PowerShell 5.0+** - Required for Windows script (Windows 10+)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Blackletter-Systems
   ```

2. **Verify Python installation:**
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Test the tools:**
   ```bash
   # Test Python tools
   python tools/context_engineering_automation.py "Test task"
   
   # Test PowerShell (Windows)
   .\tools\context_engineering.ps1 -Action help
   ```

## 📋 Usage Workflows

### For Development Agents

1. **Before starting a task:**
   ```bash
   python tools/context_engineering_automation.py "Your task description" --template
   ```

2. **During implementation:**
   - Follow the generated workflow template
   - Reference the required documentation
   - Implement according to quality standards

3. **After completion:**
   ```bash
   python tools/context_engineering_validator.py your_response.txt
   ```

### For Code Review

1. **Validate agent responses:**
   ```bash
   python tools/context_engineering_validator.py agent_response.txt --output review_report.txt
   ```

2. **Check workflow compliance:**
   - Review validation report
   - Ensure all required steps are completed
   - Verify documentation references

### For Project Managers

1. **Generate task context:**
   ```bash
   python tools/context_engineering_automation.py "Complex feature description" --output task_analysis.json
   ```

2. **Assess task complexity:**
   - Review generated complexity assessment
   - Estimate effort requirements
   - Plan resource allocation

## 🎯 Quality Standards

### Validation Scoring

- **80%+ Score:** Pass (Compliant with Context Engineering workflow)
- **60-79% Score:** Warning (Partial compliance, needs improvement)
- **Below 60% Score:** Fail (Non-compliant, requires rework)

### Required Elements

1. **Workflow Steps (5/5 required):**
   - Context Assessment
   - Implementation Plan
   - Implementation
   - Documentation
   - Verification against checklist

2. **Documentation References (4/4 required):**
   - docs/Implementation.md
   - docs/project_structure.md
   - docs/UI_UX_doc.md
   - docs/Bug_tracking.md

3. **Rule Compliance:**
   - No NEVER rule violations
   - High ALWAYS rule compliance

## 🚀 Integration with CI/CD

### GitHub Actions Example

```yaml
name: Context Engineering Validation

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Validate Context Engineering
        run: |
          python tools/context_engineering_validator.py pr_description.txt --output validation_report.txt
      
      - name: Check Validation Results
        run: |
          if grep -q "FAILED" validation_report.txt; then
            echo "Context Engineering validation failed"
            exit 1
          fi
```

### Pre-commit Hook Example

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: context-engineering-validation
        name: Context Engineering Validation
        entry: python tools/context_engineering_validator.py
        language: python
        files: ^(docs|README|CHANGELOG)\.md$
```

## 🔍 Troubleshooting

### Common Issues

1. **Python not found:**
   ```bash
   # Check Python installation
   which python
   which python3
   
   # Install Python if needed
   # Windows: Download from python.org
   # macOS: brew install python
   # Linux: sudo apt-get install python3
   ```

2. **Permission denied (PowerShell):**
   ```powershell
   # Set execution policy
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Import errors:**
   ```bash
   # Install required packages
   pip install -r requirements.txt
   ```

### Getting Help

1. **Show tool help:**
   ```bash
   python tools/context_engineering_validator.py --help
   python tools/context_engineering_automation.py --help
   ```

2. **PowerShell help:**
   ```powershell
   .\tools\context_engineering.ps1 -Action help
   ```

3. **Check documentation:**
   - `docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md`
   - `docs/AGENT_CE_QUICK_REFERENCE.md`
   - `docs/AGENT_CE_ENFORCEMENT.md`

## 📚 Related Documentation

- **Framework Overview:** `docs/README.md`
- **Workflow Rules:** `docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md`
- **Quick Reference:** `docs/AGENT_CE_QUICK_REFERENCE.md`
- **Enforcement:** `docs/AGENT_CE_ENFORCEMENT.md`
- **System Prompt:** `docs/AGENT_CE_SYSTEM_PROMPT.md`

## 🤝 Contributing

To contribute to these tools:

1. Follow the Context Engineering workflow
2. Add tests for new functionality
3. Update documentation
4. Ensure backward compatibility
5. Follow Python and PowerShell best practices

## 📄 License

These tools are part of the Blackletter Systems project and follow the same licensing terms.
