# Blackletter Systems Startup Script for Windows

# Create .env file if it doesn't exist
if (-not (Test-Path -Path ".env")) {
    Write-Host "Creating .env file from .env.example..."
    if (Test-Path -Path ".env.example") {
        Copy-Item -Path ".env.example" -Destination ".env"
    } else {
        # Create minimal .env file
        @"
# Backend
DATABASE_URL=postgresql+psycopg://blackletter:blackletter@localhost:5432/blackletter
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=admin
S3_SECRET_KEY=adminadmin
S3_BUCKET=blackletter
VECTOR_PROVIDER=weaviate
WEAVIATE_URL=http://localhost:8081
SEARCH_URL=http://localhost:7700
PDF_SERVICE_URL=http://localhost:3001
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LLM=llama3.1:8b

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# n8n
N8N_URL=http://localhost:5678
N8N_USER=admin
N8N_PASS=adminadmin
"@ | Out-File -FilePath ".env" -Encoding utf8
    }
}

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        $dockerStatus = docker info 2>&1
        return $true
    } catch {
        return $false
    }
}

# Check if Docker is running
if (-not (Test-DockerRunning)) {
    Write-Host "Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Start infrastructure services with Docker Compose
Write-Host "Starting infrastructure services (PostgreSQL, MinIO, Weaviate, Meilisearch, Gotenberg, n8n)..." -ForegroundColor Cyan
docker compose up -d db minio weaviate meilisearch gotenberg n8n

# Create Python virtual environment if it doesn't exist
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
}

# Activate virtual environment and install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1
pip install -r src\backend\requirements.txt

# Start backend in a new terminal window
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { cd '$PWD'; .\.venv\Scripts\Activate.ps1; uvicorn src.backend.main:app --reload --port 8000 }"

# Install frontend dependencies and start frontend
Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location frontend
npm install
$env:NEXT_PUBLIC_API_URL = "http://localhost:8000"

Write-Host "Starting frontend server..." -ForegroundColor Cyan
npm run dev

# Return to root directory
Set-Location ..

Write-Host "Blackletter Systems is running!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "MinIO Console: http://localhost:9001 (admin/adminadmin)" -ForegroundColor Yellow
Write-Host "n8n: http://localhost:5678 (admin/adminadmin)" -ForegroundColor Yellow
