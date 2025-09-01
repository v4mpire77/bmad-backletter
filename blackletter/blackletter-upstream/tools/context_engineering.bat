@echo off
REM Context Engineering Tools - Windows Batch File
REM Provides easy access to Context Engineering tools on Windows

setlocal enabledelayedexpansion

REM Set colors for output
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "CYAN=[96m"
set "MAGENTA=[95m"
set "RESET=[0m"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo %RED%Error: Python is not installed or not in PATH%RESET%
        echo Please install Python 3.7+ and add it to your PATH
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
    )
) else (
    set "PYTHON_CMD=python"
)

echo %MAGENTA%============================================================%RESET%
echo %MAGENTA%CONTEXT ENGINEERING WORKFLOW TOOLS%RESET%
echo %MAGENTA%Blackletter Systems%RESET%
echo %MAGENTA%============================================================%RESET%
echo.

if "%1"=="" goto :show_help
if "%1"=="help" goto :show_help
if "%1"=="workflow" goto :show_workflow
if "%1"=="docs" goto :show_docs
if "%1"=="summary" goto :generate_summary
if "%1"=="template" goto :generate_template
if "%1"=="validate" goto :validate_response
if "%1"=="test" goto :test_tools

echo %YELLOW%Unknown action: %1%RESET%
echo.
goto :show_help

:show_help
echo %CYAN%Usage Examples:%RESET%
echo.
echo %GREEN%1. Generate context summary for a task:%RESET%
echo    context_engineering.bat summary "Implement user authentication"
echo.
echo %GREEN%2. Generate workflow template:%RESET%
echo    context_engineering.bat template "Add file upload component"
echo.
echo %GREEN%3. Validate agent response:%RESET%
echo    context_engineering.bat validate response.txt
echo.
echo %GREEN%4. Show Context Engineering workflow:%RESET%
echo    context_engineering.bat workflow
echo.
echo %GREEN%5. List documentation files:%RESET%
echo    context_engineering.bat docs
echo.
echo %GREEN%6. Test tools:%RESET%
echo    context_engineering.bat test
echo.
echo %CYAN%Available Actions:%RESET%
echo   summary    - Generate context summary for a task
echo   template   - Generate workflow template
echo   validate   - Validate agent response against workflow
echo   workflow   - Show Context Engineering workflow
echo   docs       - List required documentation files
echo   test       - Test all tools
echo   help       - Show this help message
echo.
echo %CYAN%Parameters:%RESET%
echo   First argument: Action to perform
echo   Second argument: Task description or file path
echo.
goto :end

:show_workflow
echo %MAGENTA%CONTEXT ENGINEERING WORKFLOW (MANDATORY)%RESET%
echo.
echo %CYAN%1. CONTEXT ASSESSMENT (ALWAYS FIRST)%RESET%
echo    • Review Implementation Plan (docs/Implementation.md)
echo    • Examine Project Structure (docs/project_structure.md)
echo    • Check UI/UX Guidelines (docs/UI_UX_doc.md)
echo    • Review Bug Tracking (docs/Bug_tracking.md)
echo.
echo %CYAN%2. IMPLEMENTATION PLAN%RESET%
echo    • Create detailed implementation plan
echo    • Identify dependencies and prerequisites
echo    • Plan testing strategy
echo.
echo %CYAN%3. IMPLEMENTATION%RESET%
echo    • Follow established patterns
echo    • Adhere to architecture
echo    • Write quality, testable code
echo.
echo %CYAN%4. DOCUMENTATION (CONCURRENT)%RESET%
echo    • Update docstrings and documentation
echo    • Maintain changelog
echo    • Document design decisions
echo.
echo %CYAN%5. VERIFICATION%RESET%
echo    • Check against quality standards
echo    • Verify workflow compliance
echo    • Run tests and validation
echo.
goto :end

:show_docs
echo %MAGENTA%REQUIRED DOCUMENTATION FILES%RESET%
echo.
echo %CYAN%Core Documentation:%RESET%
echo   • docs/Implementation.md - Overall project plan
echo   • docs/project_structure.md - File organization
echo   • docs/UI_UX_doc.md - Design system
echo   • docs/Bug_tracking.md - Known issues
echo   • docs/ARCHITECTURE.md - System architecture
echo.
echo %CYAN%Context Engineering:%RESET%
echo   • docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md - Workflow rules
echo   • docs/AGENT_CE_QUICK_REFERENCE.md - Quick reference
echo   • docs/AGENT_CE_ENFORCEMENT.md - Enforcement rules
echo   • docs/AGENT_CE_SYSTEM_PROMPT.md - System prompt template
echo.
goto :end

:generate_summary
if "%2"=="" (
    echo %RED%Error: Task description is required%RESET%
    echo Usage: context_engineering.bat summary "Your task description"
    goto :end
)
echo %CYAN%Generating context summary for task...%RESET%
echo Task: %2
echo.
%PYTHON_CMD% context_engineering_automation.py "%2" --project-root ..
if %errorlevel% equ 0 (
    echo %GREEN%Context summary generated successfully!%RESET%
) else (
    echo %RED%Failed to generate context summary%RESET%
)
goto :end

:generate_template
if "%2"=="" (
    echo %RED%Error: Task description is required%RESET%
    echo Usage: context_engineering.bat template "Your task description"
    goto :end
)
echo %CYAN%Generating workflow template...%RESET%
echo Task: %2
echo.
%PYTHON_CMD% context_engineering_automation.py "%2" --template --project-root ..
if %errorlevel% equ 0 (
    echo %GREEN%Workflow template generated successfully!%RESET%
) else (
    echo %RED%Failed to generate workflow template%RESET%
)
goto :end

:validate_response
if "%2"=="" (
    echo %RED%Error: Input file is required for validation%RESET%
    echo Usage: context_engineering.bat validate response.txt
    goto :end
)
if not exist "%2" (
    echo %RED%Error: Input file not found: %2%RESET%
    goto :end
)
echo %CYAN%Validating agent response...%RESET%
echo Input file: %2
echo.
%PYTHON_CMD% context_engineering_validator.py "%2" --project-root ..
if %errorlevel% equ 0 (
    echo %GREEN%Validation completed successfully!%RESET%
) else (
    echo %RED%Validation failed%RESET%
)
goto :end

:test_tools
echo %CYAN%Testing Context Engineering tools...%RESET%
echo.
%PYTHON_CMD% test_tools.py
if %errorlevel% equ 0 (
    echo %GREEN%All tools are working correctly!%RESET%
) else (
    echo %RED%Some tools have issues. Check the output above.%RESET%
)
goto :end

:end
echo.
echo %CYAN%For more information, see tools/README.md%RESET%
pause
