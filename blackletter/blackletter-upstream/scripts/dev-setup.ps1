# dev-setup.ps1 - Development Environment Setup
# Blackletter GDPR Processor MVP
# Context Engineering Framework v2.0.0 Compliant
# ASCII-only characters for Windows compatibility

param(
    [switch]$SkipPython = $false,
    [switch]$SkipNode = $false,
    [switch]$SkipDocker = $false
)

$ErrorActionPreference = "Stop"

Write-Host "Blackletter GDPR Processor - Development Setup" -ForegroundColor Green
Write-Host "Context Engineering Framework v2.0.0" -ForegroundColor Cyan
Write-Host "ASCII-only PowerShell script for Windows compatibility" -ForegroundColor Gray

# Step 1: Check Prerequisites
Write-Host "`nStep 1: Checking Prerequisites..." -ForegroundColor Yellow

if (-not $SkipPython) {
    Write-Host "Checking Python..." -ForegroundColor White
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "Found: $pythonVersion" -ForegroundColor Green
        
        if ($pythonVersion -notmatch "Python 3\.(9|10|11|12)") {
            Write-Warning "Python 3.9+ recommended. Current: $pythonVersion"
        }
    } catch {
        Write-Error "Python not found. Install Python 3.9+ and add to PATH."
        exit 1
    }
}

if (-not $SkipNode) {
    Write-Host "Checking Node.js..." -ForegroundColor White
    try {
        $nodeVersion = node --version 2>&1
        Write-Host "Found: $nodeVersion" -ForegroundColor Green
        
        $nodeVersionNumber = [int]($nodeVersion -replace "v(\d+)\..*", '$1')
        if ($nodeVersionNumber -lt 18) {
            Write-Warning "Node.js 18+ recommended. Current: $nodeVersion"
        }
    } catch {
        Write-Error "Node.js not found. Install Node.js 18+ and add to PATH."
        exit 1
    }
}

if (-not $SkipDocker) {
    Write-Host "Checking Docker..." -ForegroundColor White
    try {
        $dockerVersion = docker --version 2>&1
        Write-Host "Found: $dockerVersion" -ForegroundColor Green
        
        # Check if Docker is running
        docker info > $null 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Docker is installed but not running. Please start Docker Desktop."
        }
    } catch {
        Write-Warning "Docker not found. Install Docker Desktop for container support."
    }
}

# Step 2: Backend Setup
Write-Host "`nStep 2: Setting up Backend..." -ForegroundColor Yellow

if (Test-Path "backend") {
    Set-Location "backend"
    
    # Create virtual environment
    Write-Host "Creating Python virtual environment..." -ForegroundColor White
    if (Test-Path "venv") {
        Write-Host "Virtual environment already exists" -ForegroundColor Gray
    } else {
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to create virtual environment"
            exit 1
        }
        Write-Host "Virtual environment created" -ForegroundColor Green
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor White
    & "venv\Scripts\Activate.ps1"
    
    # Install dependencies
    Write-Host "Installing Python dependencies..." -ForegroundColor White
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Backend dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Error "Failed to install backend dependencies"
        exit 1
    }
    
    Set-Location ".."
} else {
    Write-Warning "Backend directory not found"
}

# Step 3: Frontend Setup
Write-Host "`nStep 3: Setting up Frontend..." -ForegroundColor Yellow

if (Test-Path "frontend") {
    Set-Location "frontend"
    
    # Install Node.js dependencies
    Write-Host "Installing Node.js dependencies..." -ForegroundColor White
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Frontend dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Error "Failed to install frontend dependencies"
        exit 1
    }
    
    Set-Location ".."
} else {
    Write-Warning "Frontend directory not found"
}

# Step 4: Environment Configuration
Write-Host "`nStep 4: Environment Configuration..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "Copying .env.example to .env..." -ForegroundColor White
        Copy-Item ".env.example" ".env"
        Write-Host "Please edit .env file with your configuration" -ForegroundColor Yellow
    } else {
        Write-Warning ".env.example not found"
    }
} else {
    Write-Host ".env file already exists" -ForegroundColor Gray
}

# Step 5: Docker Setup
if (-not $SkipDocker) {
    Write-Host "`nStep 5: Docker Setup..." -ForegroundColor Yellow
    
    if (Test-Path "docker-compose.yml") {
        Write-Host "Building Docker images..." -ForegroundColor White
        docker-compose build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker images built successfully" -ForegroundColor Green
        } else {
            Write-Warning "Docker build failed - continuing without Docker"
        }
    } else {
        Write-Warning "docker-compose.yml not found"
    }
}

# Step 6: Validation
Write-Host "`nStep 6: Setup Validation..." -ForegroundColor Yellow

# Check if Context Engineering tool exists
if (Test-Path "tools\context_engineering.ps1") {
    Write-Host "Running Context Engineering Framework validation..." -ForegroundColor White
    & "tools\context_engineering.ps1" -Action validate
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Context Engineering Framework validation passed" -ForegroundColor Green
    } else {
        Write-Warning "Context Engineering Framework validation failed"
    }
} else {
    Write-Warning "Context Engineering validation tool not found"
}

# Final Summary
Write-Host "`nSetup Summary:" -ForegroundColor Cyan
Write-Host "Backend: Python virtual environment and dependencies" -ForegroundColor White
Write-Host "Frontend: Node.js dependencies installed" -ForegroundColor White
Write-Host "Environment: .env configuration file" -ForegroundColor White

if (-not $SkipDocker) {
    Write-Host "Docker: Images built and ready" -ForegroundColor White
}

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your Supabase credentials" -ForegroundColor White
Write-Host "2. Run: docker-compose up -d (for Docker)" -ForegroundColor White
Write-Host "3. Or run backend and frontend separately:" -ForegroundColor White
Write-Host "   Backend: cd backend && uvicorn main:app --reload" -ForegroundColor Gray
Write-Host "   Frontend: cd frontend && npm run dev" -ForegroundColor Gray
Write-Host "4. Open http://localhost:3000 in browser" -ForegroundColor White

Write-Host "`nDEVELOPMENT SETUP COMPLETE" -ForegroundColor Green