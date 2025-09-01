# Blackletter Systems Deployment Script for Render.com

# Check if render-cli is installed
$renderCliInstalled = $null
try {
    $renderCliInstalled = Get-Command render -ErrorAction SilentlyContinue
} catch {
    # Command not found
}

if (-not $renderCliInstalled) {
    Write-Host "Render CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g @render/cli
}

# Check if logged in to Render
$loggedIn = $false
try {
    $renderWhoami = render whoami 2>&1
    if ($renderWhoami -match "Logged in as") {
        $loggedIn = $true
    }
} catch {
    # Not logged in
}

if (-not $loggedIn) {
    Write-Host "Please log in to Render:" -ForegroundColor Yellow
    render login
}

# Deploy using Blueprint
Write-Host "Deploying to Render.com..." -ForegroundColor Cyan
render blueprint launch

Write-Host "Deployment initiated!" -ForegroundColor Green
Write-Host "Check your Render dashboard for deployment status: https://dashboard.render.com" -ForegroundColor Yellow
Write-Host "Once deployed, your application will be available at: https://blackletter.onrender.com" -ForegroundColor Yellow
