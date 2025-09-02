# Context Engineering Tools

This directory contains tools and utilities to help agents follow the Context Engineering workflow and ensure compliance with the Blackletter Systems development standards.

## 🚀 Available Tools

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
CONTEXT ENGINEERING WORKFLOW VALIDATION REPORT

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
```
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
```
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

### 4. BMAD-Enhanced Context Engineering Validator (`bmad_context_engineering_validator.py`)

**Purpose:** Validates agent responses against the BMAD-enhanced Context Engineering workflow, including business context assessment, risk management, and advanced elicitation techniques.

**Features:**
- Checks for BMAD-enhanced workflow steps
- Validates business context documentation references
- Ensures BMAD rule compliance
- Generates detailed validation reports with BMAD metrics
- Provides BMAD-specific improvement recommendations

**Usage:**
```bash
# Validate from file
python tools/bmad_context_engineering_validator.py response.txt

# Validate from stdin
python tools/bmad_context_engineering_validator.py -

# Output to file
python tools/bmad_context_engineering_validator.py response.txt --output bmad_validation_report.txt

# JSON output
python tools/bmad_context_engineering_validator.py response.txt --json
```

**Output Example:**
```
BMAD-ENHANCED CONTEXT ENGINEERING WORKFLOW VALIDATION REPORT

Overall Score: 92.5% ✅ PASSED

📋 WORKFLOW COMPLIANCE
Status: ✅ Complete
Found: 6/6 steps

🚀 BMAD ENHANCEMENT COMPLIANCE
Status: ✅ Complete
Found: 3/3 enhancements

📚 DOCUMENTATION REFERENCES
Status: ✅ Complete
Referenced: 8/8 files

🔒 RULE COMPLIANCE
Score: 95.0%
ALWAYS Rules Found: 12/15

💡 ADVANCED ELICITATION COMPLIANCE
Score: 85.0%
Methods Found: 7/13

💼 BUSINESS VALUE DOCUMENTATION
Score: 90.0%
Status: ✅ Complete

🧠 KNOWLEDGE TRANSFER DOCUMENTATION
Score: 80.0%
Status: ✅ Complete

💡 RECOMMENDATIONS
• Apply additional advanced elicitation techniques
• Enhance knowledge transfer documentation
```

### 5. BMAD-Enhanced Context Engineering Automation (`bmad_context_engineering_automation.py`)

**Purpose:** Automates the BMAD-enhanced Context Engineering workflow, including business context assessment, risk analysis, and advanced elicitation techniques.

**Features:**
- Analyzes task complexity and business impact
- Identifies BMAD-relevant documentation
- Generates BMAD-enhanced implementation guidance
- Creates BMAD workflow templates
- Provides advanced elicitation options
- Includes business value assessment

**Usage:**
```bash
# Generate BMAD-enhanced context summary
python tools/bmad_context_engineering_automation.py "Implement user authentication"

# Generate BMAD workflow template
python tools/bmad_context_engineering_automation.py "Add file upload component" --template

# Save to file
python tools/bmad_context_engineering_automation.py "Create RAG endpoint" --output bmad_context.json

# Specify project root
python tools/bmad_context_engineering_automation.py "Update UI component" --project-root /path/to/project
```

**Output Example:**
```
{
  "task_analysis": {
    "description": "Implement user authentication",
    "type": "backend",
    "complexity": "MEDIUM",
    "estimated_effort": "4-8 hours",
    "business_impact": "HIGH"
  },
  "business_context_assessment": {
    "stakeholder_needs": "Analyze business requirements document",
    "value_proposition": "Review business value assessment",
    "impact_level": "HIGH"
  },
  "advanced_elicitation": {
    "methods": [
      "Expand or Contract for Audience",
      "Critique and Refine",
      "Tree of Thoughts"
    ],
    "when_to_apply": "After drafting implementation"
  }
}
```

### 6. BMAD-Enhanced PowerShell Script (`bmad_context_engineering.ps1`)

**Purpose:** Provides easy access to BMAD-enhanced Context Engineering tools on Windows systems with BMAD-specific features.

**Features:**
- Windows-native interface with BMAD color coding
- Color-coded output for BMAD elements
- Easy command execution for BMAD workflows
- Built-in help and BMAD examples
- Business context analysis capabilities

**Usage:**
```
# Show help
.\tools\bmad_context_engineering.ps1

# Generate BMAD-enhanced context summary
.\tools\bmad_context_engineering.ps1 -Task "Implement user authentication" -Action summary

# Generate BMAD workflow template
.\tools\bmad_context_engineering.ps1 -Task "Add file upload component" -Action template

# Validate response against BMAD workflow
.\tools\bmad_context_engineering.ps1 -Task "response.txt" -Action validate

# Show BMAD workflow
.\tools\bmad_context_engineering.ps1 -Action workflow

# Analyze business context
.\tools\bmad_context_engineering.ps1 -Task "Implement GDPR compliance" -Action business
```

## 🛠️ Installation and Setup

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

## 📈 Usage Workflows

### For Development Agents

1. **Before starting a task:**
   ```bash
   python tools/bmad_context_engineering_automation.py "Your task description" --template
   ```

2. **During implementation:**
   - Follow the generated workflow template
   - Reference the required documentation
   - Implement according to quality standards
   - Apply BMAD business context assessment
   - Use advanced elicitation techniques

3. **After completion:**
   ```bash
   python tools/bmad_context_engineering_validator.py your_response.txt
   ```

### For Code Review

1. **Validate agent responses:**
   ```bash
   python tools/bmad_context_engineering_validator.py agent_response.txt --output review_report.txt
   ```

2. **Check workflow compliance:**
   - Review validation report
   - Ensure all required steps are completed
   - Verify documentation references
   - Confirm BMAD enhancements are applied

### For Project Managers

1. **Generate task context:**
   ```bash
   python tools/bmad_context_engineering_automation.py "Complex feature description" --output task_analysis.json
   ```

2. **Assess task complexity:**
   - Review generated complexity assessment
   - Estimate effort requirements
   - Plan resource allocation
   - Consider business impact

## 📊 Quality Standards

### Validation Scoring

- **80%+ Score:** Pass (Compliant with Context Engineering workflow)
- **60-79% Score:** Warning (Partial compliance, needs improvement)
- **Below 60% Score:** Fail (Non-compliant, requires rework)

### Required Elements

1. **Workflow Steps (6/6 required for BMAD):**
   - Business Context Assessment
   - Technical Context Assessment
   - Risk and Compatibility Analysis
   - Code Implementation
   - Documentation
   - Verification against checklist

2. **Documentation References (8/8 required for BMAD):**
   - docs/Business_Requirements.md
   - docs/Business_Value_Assessment.md
   - docs/Implementation.md
   - docs/project_structure.md
   - docs/UI_UX_doc.md
   - docs/Bug_tracking.md
   - docs/ARCHITECTURE.md
   - docs/Risk_Management_Framework.md

3. **Rule Compliance:**
   - No NEVER rule violations
   - High ALWAYS rule compliance
   - BMAD-specific rule adherence

## 🔄 Integration with CI/CD

### GitHub Actions Example

```
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
          python tools/bmad_context_engineering_validator.py pr_description.txt --output validation_report.txt

      - name: Check Validation Results
        run: |
          if grep -q "FAILED" validation_report.txt; then
            echo "Context Engineering validation failed"
            exit 1
          fi
```

### Pre-commit Hook Example

```
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: context-engineering-validation
        name: Context Engineering Validation
        entry: python tools/bmad_context_engineering_validator.py
        language: python
        files: ^(?:docs|README|CHANGELOG)\.md$
```

## 🔧 Troubleshooting

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
   ```
   # Set execution policy
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Import errors:**
   ```
   # Install required packages
   pip install -r requirements.txt
   ```

### Getting Help

1. **Show tool help:**
   ```
   python tools/bmad_context_engineering_validator.py --help
   python tools/bmad_context_engineering_automation.py --help
   ```

2. **PowerShell help:**
   ```
   .\tools\bmad_context_engineering.ps1 -Action help
   ```

3. **Check documentation:**
   - `docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md`
   - `docs/AGENT_CE_QUICK_REFERENCE.md`
   - `docs/AGENT_CE_ENFORCEMENT.md`
   - `docs/BMAD_ADVANCED_ELICITATION_GUIDELINES.md`

## 📚 Related Documentation

- **Framework Overview:** `docs/README.md`
- **Workflow Rules:** `docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md`
- **Quick Reference:** `docs/AGENT_CE_QUICK_REFERENCE.md`
- **Enforcement:** `docs/AGENT_CE_ENFORCEMENT.md`
- **System Prompt:** `docs/AGENT_CE_SYSTEM_PROMPT.md`
- **BMAD Method:** `BMAD-METHOD-main/dist/agents/bmad-master.txt`

## 🤝 Contributing

To contribute to these tools:

1. Follow the Context Engineering workflow
2. Add tests for new functionality
3. Update documentation
4. Ensure backward compatibility
5. Follow Python and PowerShell best practices

## 📄 License

These tools are part of the Blackletter Systems project and follow the same licensing terms.
