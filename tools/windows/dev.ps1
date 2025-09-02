<#
  Run API and/or Web dev servers on Windows.
  Usage:
    .\tools\windows\dev.ps1 -Api   # backend only
    .\tools\windows\dev.ps1 -Web   # frontend only
    .\tools\windows\dev.ps1        # both
#>
param(
    [switch]$Api,
    [switch]$Web
)

if (-not ($Api.IsPresent -or $Web.IsPresent)) {
    $Api = $true
    $Web = $true
}

$apiScript = {
    Write-Host "Starting FastAPI API server..."
    if (-not (Test-Path ".venv")) {
        Write-Error "Virtual environment not found. Run tools\\windows\\setup.ps1 first."
        return
    }
    . .\.venv\Scripts\Activate.ps1
    $env:PYTHONPATH = ".;./apps/api"
    uvicorn blackletter_api.main:app --reload --app-dir apps/api
}

$webScript = {
    Write-Host "Starting Next.js web server..."
    Push-Location "apps/web"
    pnpm dev
    Pop-Location
}

$jobs = @()
if ($Api) { $jobs += Start-Job -ScriptBlock $apiScript }
if ($Web) { $jobs += Start-Job -ScriptBlock $webScript }

Write-Host "Development servers are starting. Press Ctrl+C to stop." -ForegroundColor Green
while ($jobs.State -contains "Running") {
    foreach ($job in $jobs) { Receive-Job $job }
    Start-Sleep -Milliseconds 200
}
Remove-Job -Force -State Completed,Failed,Stopped
