<#
  Blackletter Dev Setup (Windows PowerShell)

  Usage:
    - Right click -> Run with PowerShell, or
    - In terminal:  pwsh -NoProfile -File ./setup.ps1

  What this does:
    - Creates a local Python virtual environment in .venv
    - Installs Python dependencies from requirements.txt
    - Copies .env.example -> .env if missing
    - Creates local data folders under .data/analyses
    - Prints handy dev commands
#>

param(
  [switch]$RecreateVenv,
  [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'

function Write-Step($msg) { Write-Host "[>] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[✓] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[!] $msg" -ForegroundColor Yellow }

Write-Step "Detecting Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $python) { throw 'Python not found. Install Python 3.11+ and ensure it is on PATH.' }
$pyVersion = & $python --version
Write-Ok "Using $pyVersion"

$venvPath = Join-Path $PSScriptRoot '.venv'
if (Test-Path $venvPath -and $RecreateVenv) {
  Write-Warn "Recreating virtual environment..."
  Remove-Item -Recurse -Force $venvPath
}

if (-not (Test-Path $venvPath)) {
  Write-Step "Creating virtual environment at .venv"
  & $python -m venv $venvPath
  Write-Ok "Virtual environment created"
} else {
  Write-Ok ".venv already exists"
}

$pip = Join-Path $venvPath 'Scripts' 'pip.exe'
$py  = Join-Path $venvPath 'Scripts' 'python.exe'
if (-not (Test-Path $pip)) { throw 'pip executable not found in .venv. Did venv creation fail?' }

if (-not $SkipInstall) {
  Write-Step "Upgrading pip"
  & $py -m pip install --upgrade pip | Out-Host
  Write-Step "Installing Python dependencies from requirements.txt"
  & $pip install -r (Join-Path $PSScriptRoot 'requirements.txt') | Out-Host
  Write-Ok "Dependencies installed"
} else {
  Write-Warn "Skipping dependency install by request"
}

Write-Step "Ensuring .env exists"
$envFile = Join-Path $PSScriptRoot '.env'
$envExample = Join-Path $PSScriptRoot '.env.example'
if (-not (Test-Path $envFile)) {
  if (Test-Path $envExample) {
    Copy-Item $envExample $envFile
    Write-Ok "Created .env from .env.example"
  } else {
    # Create a reasonable default
    @(
      'CORS_ORIGINS=*',
      'DATA_ROOT=.data',
      'JOB_SYNC=0',
      'ANALYSES_FS_ENABLED=0',
      '# DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/blackletter'
    ) | Set-Content -Path $envFile -Encoding UTF8
    Write-Ok "Created .env with defaults"
  }
} else {
  Write-Ok ".env already present"
}

Write-Step "Ensuring data directories exist"
$dataDir = Join-Path $PSScriptRoot '.data'
$analyses = Join-Path $dataDir 'analyses'
New-Item -ItemType Directory -Force -Path $analyses | Out-Null
Write-Ok "Data folders ready at .data/analyses"

Write-Host ""; Write-Ok "Setup complete."
Write-Host ""; Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1) Activate venv:" -NoNewline; Write-Host " .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  2) Run API:" -NoNewline; Write-Host " uvicorn blackletter_api.main:app --reload --app-dir apps/api" -ForegroundColor Yellow
Write-Host "  3) (Optional) Run tests:" -NoNewline; Write-Host " .\.venv\Scripts\python.exe -m pytest apps/api/blackletter_api/tests -q" -ForegroundColor Yellow
Write-Host ""; Write-Host "Toggles:" -ForegroundColor Cyan
Write-Host "  JOB_SYNC=1 (synchronous jobs)" -ForegroundColor Gray
Write-Host "  ANALYSES_FS_ENABLED=1 (list analyses from filesystem)" -ForegroundColor Gray

