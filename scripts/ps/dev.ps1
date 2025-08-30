param(
    [int]$Port = 8000,
    [string]$Host = "127.0.0.1"
)

Write-Host "Creating virtual environment (if missing) and starting API..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    py -3.11 -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt

$env:JOB_SYNC = "1"  # sync processing for local dev

uvicorn blackletter_api.main:app --app-dir apps\api --reload --host $Host --port $Port

