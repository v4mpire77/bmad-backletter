# BMAD-Enhanced Context Engineering PowerShell Script
# Provides easy access to BMAD-enhanced Context Engineering tools and validation

param(
    [Parameter(Mandatory=$false)]
    [string]$Task,

    [Parameter(Mandatory=$false)]
    [string]$Action = "help",

    [Parameter(Mandatory=$false)]
    [string]$Output,

    [Parameter(Mandatory=$false)]
    [switch]$Template,

    [Parameter(Mandatory=$false)]
    [switch]$Validate,

    [Parameter(Mandatory=$false)]
    [switch]$BusinessContext
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
    BMAD = "Blue"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Show-Header {
    Write-ColorOutput "=" * 70 "Header"
    Write-ColorOutput "BMAD-ENHANCED CONTEXT ENGINEERING WORKFLOW TOOLS" "Header"
    Write-ColorOutput "Blackletter Systems with Business Model Analysis and Design (BMAD)" "Header"
    Write-ColorOutput "=" * 70 "Header"
    Write-Host ""
}

function Show-Help {
    Write-ColorOutput "Usage Examples:" "Info"
    Write-Host ""
    Write-ColorOutput "1. Generate BMAD-enhanced context summary for a task:" "Success"
    Write-Host "   .\bmad_context_engineering.ps1 -Task 'Implement user authentication' -Action summary"
    Write-Host ""
    Write-ColorOutput "2. Generate BMAD-enhanced workflow template:" "Success"
    Write-Host "   .\bmad_context_engineering.ps1 -Task 'Add file upload component' -Template"
    Write-Host ""
    Write-ColorOutput "3. Validate agent response against BMAD-enhanced workflow:" "Success"
    Write-Host "   .\bmad_context_engineering.ps1 -Action validate -Input 'response.txt'"
    Write-Host ""
    Write-ColorOutput "4. Show BMAD-enhanced Context Engineering workflow:" "Success"
    Write-Host "   .\bmad_context_engineering.ps1 -Action workflow"
    Write-Host ""
    Write-ColorOutput "5. Analyze business context for a task:" "Success"
    Write-Host "   .\bmad_context_engineering.ps1 -Task 'Implement GDPR compliance' -BusinessContext"
    Write-Host ""

    Write-ColorOutput "Available Actions:" "Info"
    Write-Host "  summary         - Generate BMAD-enhanced context summary for a task"
    Write-Host "  template        - Generate BMAD-enhanced workflow template"
    Write-Host "  validate        - Validate agent response against BMAD-enhanced workflow"
    Write-Host "  workflow        - Show BMAD-enhanced Context Engineering workflow"
    Write-Host "  docs            - List required documentation files"
    Write-Host "  business        - Analyze business context and value"
    Write-Host "  elicitation     - Apply advanced elicitation techniques"
    Write-Host "  help            - Show this help message"
    Write-Host ""

    Write-ColorOutput "Parameters:" "Info"
    Write-Host "  -Task           - Description of the task to analyze"
    Write-Host "  -Action         - Action to perform (default: help)"
    Write-Host "  -Output         - Output file path"
    Write-Host "  -Template       - Generate workflow template"
    Write-Host "  -Validate       - Validate agent response"
    Write-Host "  -BusinessContext - Focus on business context analysis"
}

function Show-Workflow {
    Write-ColorOutput "BMAD-ENHANCED CONTEXT ENGINEERING WORKFLOW (MANDATORY)" "Header"
    Write-Host ""
    Write-ColorOutput "1. BUSINESS CONTEXT ASSESSMENT (ALWAYS FIRST)" "BMAD"
    Write-Host "   • Analyze Business Requirements (docs/Business_Requirements.md)"
    Write-Host "   • Review Implementation Plan (docs/Implementation.md)"
    Write-Host "   • Assess Business Value (docs/Business_Value_Assessment.md)"
    Write-Host ""
    Write-ColorOutput "2. TECHNICAL CONTEXT ASSESSMENT" "Info"
    Write-Host "   • Examine Project Structure (docs/project_structure.md)"
    Write-Host "   • Check UI/UX Guidelines (docs/UI_UX_doc.md)"
    Write-Host "   • Review Bug Tracking (docs/Bug_tracking.md)"
    Write-Host ""
    Write-ColorOutput "3. RISK AND COMPATIBILITY ANALYSIS" "BMAD"
    Write-Host "   • Identify Technical Risks (docs/Risk_Management_Framework.md)"
    Write-Host "   • Define Compatibility Requirements"
    Write-Host "   • Document Mitigation Strategies"
    Write-Host ""
    Write-ColorOutput "4. CODE IMPLEMENTATION" "Info"
    Write-Host "   • Follow Established Patterns"
    Write-Host "   • Adhere to Architecture"
    Write-Host "   • Implement with Quality"
    Write-Host "   • Ensure Testability"
    Write-Host "   • Maintain Business Focus (BMAD-Enhanced)"
    Write-Host "   • Apply Advanced Elicitation Techniques (BMAD-Enhanced)"
    Write-Host "   • Document Business Value Delivery (BMAD-Enhanced)"
    Write-Host ""
    Write-ColorOutput "5. DOCUMENTATION (CONCURRENT)" "Info"
    Write-Host "   • Update Documentation"
    Write-Host "   • Maintain Changelog"
    Write-Host "   • Knowledge Transfer (BMAD-Enhanced)"
    Write-Host ""
    Write-ColorOutput "6. VERIFICATION" "Info"
    Write-Host "   • Check against quality standards"
    Write-Host "   • Verify workflow compliance"
    Write-Host "   • Run tests and validation"
    Write-Host "   • Validate Business Success Criteria (BMAD-Enhanced)"
}

function Show-Documentation {
    Write-ColorOutput "REQUIRED DOCUMENTATION FILES" "Header"
    Write-Host ""
    Write-ColorOutput "Core Documentation:" "Info"
    Write-Host "  • docs/Business_Requirements.md - Business context and stakeholder needs"
    Write-Host "  • docs/Business_Value_Assessment.md - Business impact evaluation criteria"
    Write-Host "  • docs/Implementation.md - Overall project plan"
    Write-Host "  • docs/project_structure.md - File organization"
    Write-Host "  • docs/UI_UX_doc.md - Design system"
    Write-Host "  • docs/Bug_tracking.md - Known issues"
    Write-Host "  • docs/ARCHITECTURE.md - System architecture"
    Write-Host "  • docs/Risk_Management_Framework.md - Risk assessment and mitigation strategies"
    Write-Host ""
    Write-ColorOutput "Context Engineering:" "Info"
    Write-Host "  • docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md - Workflow rules"
    Write-Host "  • docs/AGENT_CE_QUICK_REFERENCE.md - Quick reference"
    Write-Host "  • docs/AGENT_CE_ENFORCEMENT.md - Enforcement rules"
    Write-Host "  • docs/AGENT_CE_SYSTEM_PROMPT.md - System prompt template"
    Write-Host ""
    Write-ColorOutput "BMAD Documentation:" "BMAD"
    Write-Host "  • docs/BMAD_ADVANCED_ELICITATION_GUIDELINES.md - Advanced elicitation techniques"
    Write-Host "  • docs/BMAD_BROWNFIELD_DEVELOPMENT_APPROACH.md - Brownfield development approach"
    Write-Host "  • docs/BMAD_BUSINESS_LOGIC_DOCUMENTATION_REQUIREMENTS.md - Business logic documentation"
}

function Invoke-PythonTool {
    param(
        [string]$Tool,
        [string]$Arguments
    )

    try {
        # Check if Python is available
        $pythonPath = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonPath) {
            $pythonPath = Get-Command python3 -ErrorAction SilentlyContinue
        }

        if (-not $pythonPath) {
            throw "Python is not installed or not in PATH"
        }

        # Execute Python tool
        $command = "$($pythonPath.Source) tools/$Tool $Arguments"
        Write-ColorOutput "Executing: $command" "Info"

        $result = Invoke-Expression $command
        return $result

    } catch {
        Write-ColorOutput "Error executing Python tool: $_" "Error"
        return $null
    }
}

function New-ContextSummary {
    param([string]$TaskDescription)

    if (-not $TaskDescription) {
        Write-ColorOutput "Error: Task description is required" "Error"
        return
    }

    Write-ColorOutput "Generating BMAD-enhanced context summary for task..." "Info"
    Write-Host "Task: $TaskDescription"
    Write-Host ""

    $args = "--project-root ."
    if ($Output) {
        $args += " --output $Output"
    }

    $result = Invoke-PythonTool "bmad_context_engineering_automation.py" "$TaskDescription $args"

    if ($result) {
        Write-ColorOutput "BMAD-enhanced context summary generated successfully!" "Success"
    } else {
        Write-ColorOutput "Failed to generate BMAD-enhanced context summary" "Error"
    }
}

function New-WorkflowTemplate {
    param([string]$TaskDescription)

    if (-not $TaskDescription) {
        Write-ColorOutput "Error: Task description is required" "Error"
        return
    }

    Write-ColorOutput "Generating BMAD-enhanced workflow template..." "Info"
    Write-Host "Task: $TaskDescription"
    Write-Host ""

    $args = "--template --project-root ."
    if ($Output) {
        $args += " --output $Output"
    }

    $result = Invoke-PythonTool "bmad_context_engineering_automation.py" "$TaskDescription $args"

    if ($result) {
        Write-ColorOutput "BMAD-enhanced workflow template generated successfully!" "Success"
    } else {
        Write-ColorOutput "Failed to generate BMAD-enhanced workflow template" "Error"
    }
}

function Test-ResponseValidation {
    param([string]$InputFile)

    if (-not $InputFile) {
        Write-ColorOutput "Error: Input file is required for validation" "Error"
        return
    }

    if (-not (Test-Path $InputFile)) {
        Write-ColorOutput "Error: Input file not found: $InputFile" "Error"
        return
    }

    Write-ColorOutput "Validating agent response against BMAD-enhanced workflow..." "Info"
    Write-Host "Input file: $InputFile"
    Write-Host ""

    $args = "--project-root ."
    if ($Output) {
        $args += " --output $Output"
    }

    $result = Invoke-PythonTool "bmad_context_engineering_validator.py" "$InputFile $args"

    if ($result) {
        Write-ColorOutput "BMAD-enhanced validation completed successfully!" "Success"
    } else {
        Write-ColorOutput "BMAD-enhanced validation failed" "Error"
    }
}

function Analyze-BusinessContext {
    param([string]$TaskDescription)

    if (-not $TaskDescription) {
        Write-ColorOutput "Error: Task description is required" "Error"
        return
    }

    Write-ColorOutput "Analyzing business context for task..." "BMAD"
    Write-Host "Task: $TaskDescription"
    Write-Host ""

    $args = "--business-context --project-root ."
    if ($Output) {
        $args += " --output $Output"
    }

    $result = Invoke-PythonTool "bmad_context_engineering_automation.py" "$TaskDescription $args"

    if ($result) {
        Write-ColorOutput "Business context analysis completed successfully!" "Success"
    } else {
        Write-ColorOutput "Failed to analyze business context" "Error"
    }
}

function Apply-AdvancedElicitation {
    param([string]$TaskDescription)

    if (-not $TaskDescription) {
        Write-ColorOutput "Error: Task description is required" "Error"
        return
    }

    Write-ColorOutput "Applying advanced elicitation techniques..." "BMAD"
    Write-Host "Task: $TaskDescription"
    Write-Host ""

    $args = "--elicitation --project-root ."
    if ($Output) {
        $args += " --output $Output"
    }

    $result = Invoke-PythonTool "bmad_context_engineering_automation.py" "$TaskDescription $args"

    if ($result) {
        Write-ColorOutput "Advanced elicitation applied successfully!" "Success"
    } else {
        Write-ColorOutput "Failed to apply advanced elicitation" "Error"
    }
}

# Main execution
try {
    Show-Header

    switch ($Action.ToLower()) {
        "summary" {
            New-ContextSummary -TaskDescription $Task
        }
        "template" {
            New-WorkflowTemplate -TaskDescription $Task
        }
        "validate" {
            Test-ResponseValidation -InputFile $Task
        }
        "workflow" {
            Show-Workflow
        }
        "docs" {
            Show-Documentation
        }
        "business" {
            Analyze-BusinessContext -TaskDescription $Task
        }
        "elicitation" {
            Apply-AdvancedElicitation -TaskDescription $Task
        }
        "help" {
            Show-Help
        }
        default {
            Write-ColorOutput "Unknown action: $Action" "Warning"
            Write-Host ""
            Show-Help
        }
    }

} catch {
    Write-ColorOutput "Error: $_" "Error"
    Write-Host ""
    Show-Help
    exit 1
}
