@echo off
echo 🚀 Blackletter Systems - Qoder IDE Setup
echo =======================================

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell available'" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PowerShell not available. Please install PowerShell.
    pause
    exit /b 1
)

REM Run the setup script
powershell -ExecutionPolicy Bypass -File "setup-qoder-rules.ps1" %*

pause