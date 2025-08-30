<#
  set_envs.ps1  —  One command to configure env vars for:
    - local dev (Windows user env)
    - Vercel (frontend) via Vercel CLI
    - Render (backend) via render-cli *if installed*, else prints exact UI steps

  Usage:
    .\set_envs.ps1               # defaults to 'local'
    .\set_envs.ps1 local
    .\set_envs.ps1 vercel
    .\set_envs.ps1 render
    .\set_envs.ps1 all           # local + vercel (interactive) + render (prints)

  NOTE: Don’t commit secrets. This file is fine to commit if you keep secrets in
        ENV only. If you hardcode secrets here, keep it untracked.
#>

param(
  [ValidateSet('local','vercel','render','all')]
  [string]$target = 'local'
)

# =========================
# === EDIT ME (once) ======
# =========================
$RENDER_SERVICE_NAME = 'bmad-backletter'   # Render web service name
$PYTHON_VERSION      = '3.11'

# Backend (Render/FastAPI)
$DATABASE_URL        = 'postgresql://postgres:BBpxIZ59p69WhZGG@db.idqiauohdecqidqyseve.supabase.co:5432/postgres?sslmode=require'
$OPENAI_PROVIDER     = 'none'
$OCR_ENABLED         = 'false'

# Frontend (Vercel/Next.js)
$NEXT_PUBLIC_API_URL = 'https://bmad-backletter.onrender.com'
$NEXT_PUBLIC_SUPABASE_URL  = 'https://idqiauohdecqidqyseve.supabase.co'
$NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY = 'sb_publishable__Gy8apgtJiA1-Uz3eu68gA_YP6gbhNr'

# Repo paths (adjust if different)
$FRONTEND_DIR = 'apps\web'   # Next.js app
$BACKEND_DIR  = 'apps\api'   # FastAPI app

function Has-Cli($name) { return [bool](Get-Command $name -ErrorAction SilentlyContinue) }

function Set-Local {
  Write-Host "Setting LOCAL user env vars via setx..." -ForegroundColor Cyan
  setx DATABASE_URL "$DATABASE_URL" | Out-Null
  setx OPENAI_PROVIDER "$OPENAI_PROVIDER" | Out-Null
  setx OCR_ENABLED "$OCR_ENABLED" | Out-Null
  setx PYTHON_VERSION "$PYTHON_VERSION" | Out-Null
  setx NEXT_PUBLIC_API_URL "$NEXT_PUBLIC_API_URL" | Out-Null
  setx NEXT_PUBLIC_SUPABASE_URL "$NEXT_PUBLIC_SUPABASE_URL" | Out-Null
  setx NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY "$NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY" | Out-Null

  Write-Host "Done. Restart your terminal to load new variables." -ForegroundColor Green
  Write-Host "Quick check after restart:" -ForegroundColor Yellow
  Write-Host '  echo $env:DATABASE_URL'
  Write-Host '  echo $env:NEXT_PUBLIC_API_URL'
}

function Set-Vercel {
  if (-not (Has-Cli 'vercel')) {
    Write-Host "`nVercel CLI not found. Install: npm i -g vercel" -ForegroundColor Yellow
    return
  }
  Write-Host "`nSetting Vercel project envs (interactive adds)..." -ForegroundColor Cyan
  Push-Location $FRONTEND_DIR
  try {
    vercel login | Out-Null
    # Each add is interactive; we pipe values to avoid manual typing
    cmd /c "echo $NEXT_PUBLIC_API_URL| vercel env add NEXT_PUBLIC_API_URL production"
    cmd /c "echo $NEXT_PUBLIC_API_URL| vercel env add NEXT_PUBLIC_API_URL preview"
    cmd /c "echo $NEXT_PUBLIC_SUPABASE_URL| vercel env add NEXT_PUBLIC_SUPABASE_URL production"
    cmd /c "echo $NEXT_PUBLIC_SUPABASE_URL| vercel env add NEXT_PUBLIC_SUPABASE_URL preview"
    cmd /c "echo $NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY| vercel env add NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY production"
    cmd /c "echo $NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY| vercel env add NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY preview"

    Write-Host "`nVercel envs added. Redeploy from Vercel dashboard (or run 'vercel --prod')." -ForegroundColor Green
  } finally {
    Pop-Location
  }
}

function Set-Render {
  # Two routes: render-cli (community) OR print exact UI steps
  if (Has-Cli 'render') {
    Write-Host "`nrender-cli found. Attempting to set service envs..." -ForegroundColor Cyan
    # Example commands—service slug must match. If auth needed, run `render login`.
    render login
    render env set DATABASE_URL "$DATABASE_URL" --service "$RENDER_SERVICE_NAME"
    render env set OPENAI_PROVIDER "$OPENAI_PROVIDER" --service "$RENDER_SERVICE_NAME"
    render env set OCR_ENABLED "$OCR_ENABLED" --service "$RENDER_SERVICE_NAME"
    render env set PYTHON_VERSION "$PYTHON_VERSION" --service "$RENDER_SERVICE_NAME"
    Write-Host "Render envs set. Trigger a deploy from the dashboard if not automatic." -ForegroundColor Green
  } else {
    Write-Host "`nNo render-cli detected. Do this in the UI:" -ForegroundColor Yellow
    Write-Host "  1) Render → $RENDER_SERVICE_NAME → Settings → Environment → Edit"
    Write-Host "  2) Add/Update:"
    Write-Host "       DATABASE_URL=$DATABASE_URL"
    Write-Host "       OPENAI_PROVIDER=$OPENAI_PROVIDER"
    Write-Host "       OCR_ENABLED=$OCR_ENABLED"
    Write-Host "       PYTHON_VERSION=$PYTHON_VERSION"
    Write-Host "  3) Save and Deploy."
  }
}

switch ($target) {
  'local'  { Set-Local }
  'vercel' { Set-Vercel }
  'render' { Set-Render }
  'all'    { Set-Local; Set-Vercel; Set-Render }
}

