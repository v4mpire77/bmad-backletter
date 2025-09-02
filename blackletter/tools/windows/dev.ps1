# Simple development script to run the API and Web apps.
# Usage:
#   .\tools\windows\dev.ps1 -Api      # Runs only the FastAPI backend
#   .\tools\windows\dev.ps1 -Web      # Runs only the Next.js frontend
#   .\tools\windows\dev.ps1           # Runs both concurrently

param(
    [switch]$Api,
    [switch]$Web
)

# Default to running both if no specific switch is provided
if (-not ($Api.IsPresent -or $Web.IsPresent)) {
    $Api = $true
    $Web = $true
}

$apiScript = {
    Write-Host "Starting FastAPI API server..."
    # Ensure the virtual environment is activated
    if (-not (Test-Path ".venv")) {
        Write-Error "Virtual environment not found. Please run 'py -m venv .venv' and install dependencies first."
        return
    }
    .\.venv\Scripts\Activate.ps1
    # Set PYTHONPATH to allow imports from the 'apps' directory
    $env:PYTHONPATH = ".;./apps/api"
    uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
}

$webScript = {
    Write-Host "Starting Next.js web server..."
    # Navigate to the web app directory to run pnpm
    Push-Location "apps/web"
    pnpm dev
    Pop-Location
}

$jobs = @()
if ($Api) {
    $jobs += Start-Job -ScriptBlock $apiScript
}
if ($Web) {
    $jobs += Start-Job -ScriptBlock $webScript
}

Write-Host "Development servers are starting. Press Ctrl+C to stop." -ForegroundColor Green

# Tail the logs from the running jobs
while ($jobs.State -contains "Running") {
    foreach ($job in $jobs) {
        Receive-Job $job
    }
    Start-Sleep -Milliseconds 200
}

# Cleanup
Remove-Job -Force -State Completed,Failed,Stopped
