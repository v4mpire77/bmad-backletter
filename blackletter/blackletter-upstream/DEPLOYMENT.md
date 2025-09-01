# Blackletter Systems - Deployment Guide

## Overview

This guide covers deployment options for Blackletter Systems, from local development to production environments.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (for containerized deployment)
- PostgreSQL 13+
- Redis 6+

## Local Development Setup

### 1. Backend Setup

```bash
# Clone repository
git clone https://github.com/your-org/blackletter-systems.git
cd blackletter-systems

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/blackletter"
export REDIS_URL="redis://localhost:6379"
export LLM_PROVIDER="openai"  # or "ollama"
export OPENAI_API_KEY="your-api-key"

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_URL="http://localhost:8000"

# Start development server
npm run dev
```

### 3. Services Setup

#### PostgreSQL (Docker)
```bash
docker run -d \
  --name postgres-blackletter \
  -e POSTGRES_DB=blackletter \
  -e POSTGRES_USER=blackletter \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:13
```

#### Redis (Docker)
```bash
docker run -d \
  --name redis-blackletter \
  -p 6379:6379 \
  redis:6-alpine
```

#### Ollama (Local LLM)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models
ollama pull llama2
ollama pull codellama
```

## Docker Deployment

### 1. Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: blackletter
      POSTGRES_USER: blackletter
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://blackletter:${POSTGRES_PASSWORD}@postgres/blackletter
      REDIS_URL: redis://redis:6379
      LLM_PROVIDER: ${LLM_PROVIDER}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./uploads:/app/uploads

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://blackletter:${POSTGRES_PASSWORD}@postgres/blackletter
      REDIS_URL: redis://redis:6379
      LLM_PROVIDER: ${LLM_PROVIDER}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./uploads:/app/uploads

volumes:
  postgres_data:
  redis_data:
```

### 2. Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
```

### 4. Environment Variables

Create `.env` file:

```env
# Database
POSTGRES_PASSWORD=your-secure-password
DATABASE_URL=postgresql://blackletter:your-secure-password@postgres/blackletter

# Redis
REDIS_URL=redis://redis:6379

# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# File Storage
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=/app/uploads

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### 5. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Cloud Deployment

### AWS Deployment

#### 1. ECS Fargate Setup

Create `aws/ecs-task-definition.json`:

```json
{
  "family": "blackletter-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/blackletter-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:password@rds-endpoint:5432/blackletter"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/blackletter-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 2. Infrastructure as Code (Terraform)

Create `aws/main.tf`:

```hcl
provider "aws" {
  region = "us-east-1"
}

# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

# RDS Database
resource "aws_db_instance" "blackletter" {
  identifier        = "blackletter-db"
  engine            = "postgres"
  engine_version    = "13.7"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  
  db_name  = "blackletter"
  username = "blackletter"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "blackletter-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  port                 = 6379
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "blackletter-cluster"
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "blackletter-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}
```

### Azure Deployment

#### 1. Azure Container Instances

Create `azure/deploy.sh`:

```bash
#!/bin/bash

# Create resource group
az group create --name blackletter-rg --location eastus

# Create Azure Container Registry
az acr create --resource-group blackletter-rg \
  --name blackletteracr --sku Basic

# Build and push images
az acr build --registry blackletteracr --image backend:latest ./backend
az acr build --registry blackletteracr --image frontend:latest ./frontend

# Create PostgreSQL database
az postgres flexible-server create \
  --resource-group blackletter-rg \
  --name blackletter-db \
  --admin-user blackletter \
  --admin-password $DB_PASSWORD \
  --sku-name Standard_B1ms

# Deploy backend container
az container create \
  --resource-group blackletter-rg \
  --name blackletter-backend \
  --image blackletteracr.azurecr.io/backend:latest \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL="postgresql://blackletter:$DB_PASSWORD@blackletter-db.postgres.database.azure.com/blackletter" \
    REDIS_URL="redis://blackletter-redis.redis.cache.windows.net:6380"
```

### Google Cloud Deployment

#### 1. Cloud Run Setup

Create `gcp/deploy.sh`:

```bash
#!/bin/bash

# Set project
gcloud config set project your-project-id

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Build and deploy backend
gcloud run deploy blackletter-backend \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=$DATABASE_URL,REDIS_URL=$REDIS_URL

# Build and deploy frontend
gcloud run deploy blackletter-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=$BACKEND_URL
```

## Production Considerations

### 1. Security

- **HTTPS:** Always use HTTPS in production
- **Secrets Management:** Use AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager
- **Network Security:** Implement proper firewall rules and VPC configuration
- **Authentication:** Implement JWT-based authentication
- **Rate Limiting:** Configure appropriate rate limits

### 2. Monitoring

- **Application Monitoring:** Use Sentry, DataDog, or New Relic
- **Infrastructure Monitoring:** Use CloudWatch, Azure Monitor, or Stackdriver
- **Logging:** Centralized logging with ELK stack or cloud-native solutions
- **Alerting:** Set up alerts for critical metrics

### 3. Scaling

- **Auto-scaling:** Configure auto-scaling policies
- **Load Balancing:** Use application load balancers
- **CDN:** Implement CDN for static assets
- **Database Scaling:** Consider read replicas and connection pooling

### 4. Backup & Recovery

- **Database Backups:** Automated daily backups
- **File Storage:** Versioned object storage
- **Disaster Recovery:** Multi-region deployment
- **Testing:** Regular backup restoration tests

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker build -t blackletter-backend ./backend
          docker build -t blackletter-frontend ./frontend
          
      - name: Deploy to production
        run: |
          # Deploy to your chosen platform
          echo "Deploying to production..."
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify network connectivity
   - Ensure database is running

2. **Redis Connection Issues**
   - Verify REDIS_URL format
   - Check Redis service status
   - Confirm network access

3. **File Upload Failures**
   - Check file size limits
   - Verify upload directory permissions
   - Ensure disk space availability

4. **LLM API Errors**
   - Verify API key configuration
   - Check rate limits
   - Confirm model availability

### Debug Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs backend

# Access container shell
docker-compose exec backend bash

# Check database connectivity
docker-compose exec backend python -c "import psycopg2; print('DB OK')"

# Monitor Redis
docker-compose exec redis redis-cli monitor
```

## Performance Optimization

### 1. Backend Optimization

- **Database Indexing:** Add appropriate indexes
- **Caching:** Implement Redis caching
- **Connection Pooling:** Configure database connection pools
- **Async Processing:** Use Celery for heavy tasks

### 2. Frontend Optimization

- **Code Splitting:** Implement dynamic imports
- **Image Optimization:** Use Next.js image optimization
- **Caching:** Implement service worker caching
- **Bundle Analysis:** Monitor bundle sizes

### 3. Infrastructure Optimization

- **CDN:** Use CDN for static assets
- **Load Balancing:** Implement proper load balancing
- **Auto-scaling:** Configure auto-scaling policies
- **Monitoring:** Set up performance monitoring
