# Qoder IDE Context Engineering Setup Script
# This script configures Qoder IDE to enforce Context Engineering workflow for all agents

param(
    [switch]$Validate,
    [switch]$Test,
    [switch]$Help
)

Write-Host "🚀 Blackletter Systems - Qoder IDE Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

if ($Help) {
    Write-Host @"
Qoder IDE Context Engineering Setup

USAGE:
    .\setup-qoder-rules.ps1                 # Full setup
    .\setup-qoder-rules.ps1 -Validate       # Validate current setup
    .\setup-qoder-rules.ps1 -Test           # Test agent compliance
    .\setup-qoder-rules.ps1 -Help           # Show this help

DESCRIPTION:
    This script configures Qoder IDE to enforce the Context Engineering
    workflow for all AI agents working on the Blackletter Systems project.

FEATURES:
    - Validates .cursorrules configuration
    - Tests Context Engineering tools
    - Sets up agent enforcement
    - Configures compliance validation

REQUIREMENTS:
    - Python 3.7+ installed
    - Qoder IDE 0.1.16+
    - Windows PowerShell 5.1+

"@
    exit 0
}

function Test-Prerequisites {
    Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 7) {
                Write-Host "✅ Python $pythonVersion found" -ForegroundColor Green
            } else {
                Write-Host "❌ Python 3.7+ required, found $pythonVersion" -ForegroundColor Red
                return $false
            }
        }
    }
    catch {
        Write-Host "❌ Python not found. Please install Python 3.7+" -ForegroundColor Red
        return $false
    }
    
    # Check Qoder IDE files
    if (Test-Path ".cursorrules") {
        Write-Host "✅ .cursorrules file exists" -ForegroundColor Green
    } else {
        Write-Host "❌ .cursorrules file missing" -ForegroundColor Red
        return $false
    }
    
    # Check Context Engineering tools
    if (Test-Path "tools/context_engineering_validator.py") {
        Write-Host "✅ Context Engineering validator found" -ForegroundColor Green
    } else {
        Write-Host "❌ Context Engineering validator missing" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Test-ContextEngineeringTools {
    Write-Host "🧪 Testing Context Engineering tools..." -ForegroundColor Yellow
    
    try {
        # Test automation tool
        $result = python tools/context_engineering_automation.py "test task" --validate 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Context Engineering automation tool working" -ForegroundColor Green
        } else {
            Write-Host "❌ Context Engineering automation tool failed" -ForegroundColor Red
            Write-Host $result -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Failed to test Context Engineering tools: $_" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Validate-Configuration {
    Write-Host "✅ Validating Qoder configuration..." -ForegroundColor Yellow
    
    # Check .cursorrules content
    $cursorrules = Get-Content ".cursorrules" -Raw
    
    $requiredElements = @(
        "Context Engineering Workflow",
        "MANDATORY",
        "Context Assessment",
        "Implementation Plan", 
        "Implementation",
        "Documentation",
        "Verification",
        "NEVER",
        "ALWAYS"
    )
    
    $missing = @()
    foreach ($element in $requiredElements) {
        if ($cursorrules -notmatch [regex]::Escape($element)) {
            $missing += $element
        }
    }
    
    if ($missing.Count -eq 0) {
        Write-Host "✅ .cursorrules contains all required elements" -ForegroundColor Green
    } else {
        Write-Host "❌ .cursorrules missing elements: $($missing -join ', ')" -ForegroundColor Red
        return $false
    }
    
    # Check configuration files
    if (Test-Path ".qoder-config") {
        Write-Host "✅ Qoder configuration file exists" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Qoder configuration file missing (optional)" -ForegroundColor Yellow
    }
    
    if (Test-Path ".qoder-prompt") {
        Write-Host "✅ Qoder system prompt exists" -ForegroundColor Green  
    } else {
        Write-Host "⚠️  Qoder system prompt missing (optional)" -ForegroundColor Yellow
    }
    
    return $true
}

function Show-AgentInstructions {
    Write-Host @"

🤖 AGENT INSTRUCTIONS FOR QODER IDE
===================================

To ensure all agents follow the Context Engineering workflow:

1. AGENT CONFIGURATION:
   - .cursorrules file is now configured with mandatory workflow
   - .qoder-config contains enforcement settings
   - .qoder-prompt provides system prompt template

2. REQUIRED AGENT BEHAVIOR:
   Every agent response MUST include these 5 sections:
   
   ## 1. Context Assessment
   - Review docs/Implementation.md
   - Review docs/project_structure.md  
   - Review docs/UI_UX_doc.md (frontend)
   - Review docs/Bug_tracking.md
   
   ## 2. Implementation Plan
   - Detailed plan based on context
   - Dependencies and prerequisites
   - Testing strategy
   
   ## 3. Implementation
   - Code implementation
   - Follow established patterns
   - Use existing components
   
   ## 4. Documentation
   - Update documentation
   - Maintain changelog
   - Document decisions
   
   ## 5. Verification
   - Check quality standards
   - Verify workflow compliance
   - Run tests and validation

3. VALIDATION:
   All responses will be validated with:
   python tools/context_engineering_validator.py
   
   80%+ score required for acceptance.

4. TOOLS AVAILABLE:
   - tools/context_engineering_automation.py
   - tools/context_engineering_validator.py
   - tools/context_engineering.ps1

"@ -ForegroundColor Cyan
}

# Main execution
if (-not (Test-Prerequisites)) {
    Write-Host "❌ Prerequisites check failed. Please fix the issues above." -ForegroundColor Red
    exit 1
}

if ($Validate) {
    if (Validate-Configuration) {
        Write-Host "✅ Configuration validation passed!" -ForegroundColor Green
    } else {
        Write-Host "❌ Configuration validation failed!" -ForegroundColor Red
        exit 1
    }
    exit 0
}

if ($Test) {
    if (Test-ContextEngineeringTools) {
        Write-Host "✅ Context Engineering tools test passed!" -ForegroundColor Green
    } else {
        Write-Host "❌ Context Engineering tools test failed!" -ForegroundColor Red
        exit 1
    }
    exit 0
}

# Full setup
Write-Host "🔧 Setting up Qoder IDE for Context Engineering enforcement..." -ForegroundColor Yellow

if (-not (Validate-Configuration)) {
    Write-Host "❌ Configuration validation failed during setup!" -ForegroundColor Red
    exit 1
}

if (-not (Test-ContextEngineeringTools)) {
    Write-Host "❌ Context Engineering tools test failed during setup!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Qoder IDE setup complete!" -ForegroundColor Green
Write-Host "🎉 All agents will now be required to follow Context Engineering workflow!" -ForegroundColor Green

Show-AgentInstructions

Write-Host @"

🎯 NEXT STEPS:
1. Restart Qoder IDE to load new configuration
2. Test with an agent task to verify enforcement
3. Use validation tools to check compliance
4. Review agent responses for required sections

📚 DOCUMENTATION:
- docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md
- CONTEXT_ENGINEERING_IMPLEMENTATION_COMPLETE.md
- AGENT_RULES.md
- tools/README.md

"@ -ForegroundColor White