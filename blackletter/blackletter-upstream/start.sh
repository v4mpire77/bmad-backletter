#!/bin/bash
# Blackletter Systems Startup Script for Linux/macOS

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        # Create minimal .env file
        cat > .env << EOL
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
EOL
    fi
fi

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Check if Docker is running
check_docker

# Start infrastructure services with Docker Compose
echo "Starting infrastructure services (PostgreSQL, MinIO, Weaviate, Meilisearch, Gotenberg, n8n)..."
docker compose up -d db minio weaviate meilisearch gotenberg n8n

# Create Python virtual environment if it doesn't exist
if [ ! -d .venv ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install backend dependencies
echo "Installing backend dependencies..."
source .venv/bin/activate
pip install -r src/backend/requirements.txt

# Start backend in a new terminal window
echo "Starting backend server..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && source .venv/bin/activate && uvicorn src.backend.main:app --reload --port 8000"'
else
    # Linux
    gnome-terminal -- bash -c "cd '$PWD' && source .venv/bin/activate && uvicorn src.backend.main:app --reload --port 8000; exec bash" || \
    xterm -e "cd '$PWD' && source .venv/bin/activate && uvicorn src.backend.main:app --reload --port 8000" || \
    konsole -e "cd '$PWD' && source .venv/bin/activate && uvicorn src.backend.main:app --reload --port 8000" || \
    echo "Could not open a new terminal window. Please run the backend server manually."
fi

# Install frontend dependencies and start frontend
echo "Installing frontend dependencies..."
cd frontend
npm install
export NEXT_PUBLIC_API_URL="http://localhost:8000"

echo "Starting frontend server..."
npm run dev

# Return to root directory
cd ..

echo "Blackletter Systems is running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo "MinIO Console: http://localhost:9001 (admin/adminadmin)"
echo "n8n: http://localhost:5678 (admin/adminadmin)"
