<<<<<<< HEAD
# Blackletter GDPR Processor-Obligations Checker MVP

A **Context Engineering Framework v2.0.0 compliant** system for automated detection of GDPR Article 28(3) processor obligations in contracts. Built with Next.js 14, FastAPI, Supabase, and Celery for robust, scalable contract analysis.

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Supabase account** (for cloud database)
- **PowerShell** (Windows) or **Bash** (Linux/macOS)

### 1. Clone and Setup

```bash
git clone <repository>
cd blackletter_clean
```

### 2. Environment Configuration

```powershell
# Copy environment template
copy .env.example .env

# Edit .env with your Supabase credentials
# Required: SUPABASE_URL, SUPABASE_SERVICE_KEY, DATABASE_URL
```

### 3. Automated Setup (Windows)

```powershell
# Run the automated setup script
.\scripts\dev-setup.ps1

# Validate Context Engineering compliance
.\tools\context_engineering.ps1 -Action validate
```

### 4. Start Services

**Option A: Docker (Recommended)**
```powershell
docker-compose up -d
```

**Option B: Manual**
```powershell
# Terminal 1: Backend
cd backend
venv\Scripts\Activate.ps1
uvicorn main:app --reload

# Terminal 2: Celery Worker  
cd backend
venv\Scripts\Activate.ps1
celery -A workers.celery_app worker --loglevel=info

# Terminal 3: Frontend
cd frontend
npm run dev

# Terminal 4: Redis (if not using Docker)
redis-server
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Redis**: localhost:6379

## 📋 Architecture Overview

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui | User interface and file upload |
| **Backend** | FastAPI, Pydantic, async SQLAlchemy | REST API and business logic |
| **Database** | Supabase (PostgreSQL) | Cloud database and authentication |
| **Queue** | Celery + Redis | Background job processing |
| **Container** | Docker Compose | Development environment |

### Request Flow

```mermaid
graph TB
    A[Upload Contract] --> B[FastAPI Endpoint]
    B --> C[202 Accepted + Job ID]
    B --> D[Celery Task Queue]
    D --> E[GDPR Analyzer]
    E --> F[Article 28(3) Detection]
    F --> G[Issues + Coverage]
    G --> H[Job Result Storage]
    C --> I[Status Polling]
    I --> H
    H --> J[Results Display]
```

## 🔍 GDPR Article 28(3) Analysis

The system analyzes processor contracts for compliance with all eight GDPR Article 28(3) obligations:

### Detected Obligations

| Article | Requirement | Detection Method |
|---------|-------------|------------------|
| **28(3)(a)** | Processing on documented instructions | Pattern matching + weak language detection |
| **28(3)(b)** | Personnel confidentiality commitments | Keyword detection + context analysis |
| **28(3)(c)** | Security measures (Article 32) | Technical/organizational measures detection |
| **28(3)(d)** | Sub-processor authorization | Prior consent requirement analysis |
| **28(3)(e)** | Data subject rights assistance | Rights fulfillment obligation detection |
| **28(3)(f)** | Breach notification procedures | Notification timeline and process analysis |
| **28(3)(g)** | Data deletion/return obligations | End-of-processing requirement detection |
| **28(3)(h)** | Audit and inspection rights | Access and compliance demonstration |

### Output Format

**Issues Detected:**
```json
{
  "id": "issue_abc123",
  "citation": "GDPR Article 28(3)(a)",
  "severity": "High",
  "confidence": 0.85,
  "snippet": "may process data as deemed appropriate",
  "recommendation": "Replace with specific documented instructions requirement"
}
```

**Coverage Assessment:**
```json
{
  "article": "28(3)(a)",
  "status": "Partial",
  "confidence": 0.75,
  "present": true,
  "strength": "weak"
}
```

## 🛠️ API Endpoints

### Job Management (202 Accepted Pattern)

```http
POST /api/v1/jobs/
Content-Type: multipart/form-data

→ 202 Accepted
Location: /api/v1/jobs/{job_id}/status
{
  "job_id": "uuid-here",
  "status": "pending",
  "location": "/api/v1/jobs/{job_id}/status"
}
```

```http
GET /api/v1/jobs/{job_id}/status
→ 200 OK
{
  "job_id": "uuid-here",
  "status": "processing",
  "progress": 0.5,
  "message": "Analyzing GDPR compliance"
}
```

```http
GET /api/v1/jobs/{job_id}/result
→ 200 OK (when completed)
{
  "job_id": "uuid-here",
  "analysis": {
    "issues": [...],
    "coverage": [...],
    "metadata": {...}
  }
}
```

## 🏗️ Development

### Project Structure

```
blackletter_clean/
├── backend/
│   ├── app/
│   │   ├── core/config.py          # Pydantic settings
│   │   ├── models/schemas.py       # Type definitions
│   │   ├── routers/jobs.py         # 202 Accepted API
│   │   └── services/
│   │       ├── gdpr_analyzer.py    # Article 28(3) analysis
│   │       └── job_service.py      # Job management
│   ├── workers/celery_app.py       # Background processing
│   ├── tests/fixtures/             # Golden test data
│   ├── main.py                     # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Upload interface
│   │   └── layout.tsx             # App layout
│   ├── lib/
│   │   ├── api.ts                 # Type-safe API client
│   │   ├── types.ts               # TypeScript definitions
│   │   └── utils.ts               # Helper functions
│   └── package.json
├── scripts/
│   └── dev-setup.ps1              # Development setup
├── tools/
│   └── context_engineering.ps1    # Framework validation
├── docker-compose.yml             # Container orchestration
└── .env.example                   # Environment template
```

### Testing

**Backend Tests:**
```powershell
cd backend
pytest tests/ -v --cov=app
```

**Frontend Tests:**
```powershell
cd frontend  
npm test
```

**Golden Test Validation:**
```python
# Tests against backend/tests/fixtures/processor_obligations/golden_tests.json
# Validates precision ≥85%, recall ≥90%, latency <60s
```

### Adding New GDPR Patterns

1. **Update Analyzer** (`backend/app/services/gdpr_analyzer.py`):
```python
self.obligation_patterns["28_3_new"] = {
    "name": "New Obligation",
    "strong_patterns": [r"specific\s+requirement"],
    "weak_patterns": [r"reasonable\s+efforts"]
}
```

2. **Add Test Cases** (`backend/tests/fixtures/processor_obligations/golden_tests.json`):
```json
{
  "id": "test_new_obligation",
  "category": "28_3_new",
  "contract_text": "Test contract text...",
  "expected_issues": [...],
  "expected_coverage": {...}
}
```

3. **Validate Changes**:
```powershell
.\tools\context_engineering.ps1 -Action validate
pytest backend/tests/ -k "test_gdpr_analyzer"
```

## 📊 Context Engineering Framework Compliance

This implementation achieves **>80% compliance** with Context Engineering Framework v2.0.0.

### Validation

```powershell
# Run compliance check
.\tools\context_engineering.ps1 -Action validate

# Generate compliance report
.\tools\context_engineering.ps1 -Action report
```

### Compliance Checklist

- ✅ **Docker Compose** multi-service architecture
- ✅ **202 Accepted API** pattern implementation  
- ✅ **Type Safety** with Pydantic + TypeScript
- ✅ **Async Processing** with Celery + Redis
- ✅ **Error Handling** comprehensive exception management
- ✅ **ASCII Scripts** Windows PowerShell compatibility
- ✅ **Golden Tests** GDPR pattern validation
- ✅ **Documentation** comprehensive setup guides
- ✅ **Environment Config** `.env` based configuration
- ✅ **Health Checks** service monitoring endpoints

### Framework Features

| Feature | Implementation | Compliance |
|---------|----------------|------------|
| **Agent Architecture** | Multi-service with clear separation | ✅ |
| **Error Recovery** | Retry logic + graceful degradation | ✅ |
| **Type Safety** | Pydantic + TypeScript throughout | ✅ |
| **Observability** | Logging + health checks + metrics | ✅ |
| **Scalability** | Celery workers + Redis clustering | ✅ |
| **Security** | Environment isolation + input validation | ✅ |

## 🔧 Troubleshooting

### Common Issues

**1. Context Engineering Validation Fails**
```powershell
# Check missing components
.\tools\context_engineering.ps1 -Action validate

# Common fixes:
# - Ensure all files are in correct locations
# - Verify ASCII-only characters in PowerShell scripts
# - Check Docker Compose service definitions
```

**2. Celery Workers Not Starting**
```powershell
# Check Redis connection
redis-cli ping

# Verify Celery configuration
cd backend
celery -A workers.celery_app inspect active
```

**3. GDPR Analysis Errors**
```powershell
# Check backend logs
docker-compose logs backend

# Validate test fixtures
pytest backend/tests/test_gdpr_analyzer.py -v
```

**4. Frontend Build Issues**
```powershell
# Clear Next.js cache
cd frontend
rm -rf .next node_modules
npm install
npm run build
```

### Performance Optimization

**Backend:**
- Tune Celery worker concurrency
- Implement result caching with Redis
- Optimize GDPR pattern regex compilation

**Frontend:**
- Enable Next.js static optimization
- Implement request debouncing
- Add progressive loading for large results

## 📈 Monitoring & Production

### Health Checks

- **Backend**: `GET /health`
- **Frontend**: `GET /` (Next.js health)
- **Redis**: `redis-cli ping`
- **Celery**: `celery -A workers.celery_app inspect active`

### Metrics

```json
{
  "jobs_processed": 1250,
  "avg_processing_time": "45.2s",
  "compliance_score": "87%",
  "error_rate": "2.1%"
}
```

### Production Deployment

1. **Environment Variables**: Configure production `.env`
2. **Database**: Set up Supabase production instance
3. **Scaling**: Increase Celery worker count
4. **Monitoring**: Implement Sentry/Prometheus
5. **Security**: Enable HTTPS, rate limiting

## 📝 License

**Proprietary** - Blackletter Systems  
Context Engineering Framework v2.0.0 Compliant

---

## 🤝 Contributing

1. **Framework Compliance**: Maintain 80%+ compliance score
2. **Type Safety**: All new code must be typed (Pydantic/TypeScript)
3. **ASCII Scripts**: PowerShell scripts must be ASCII-only
4. **Golden Tests**: Update test fixtures for new patterns
5. **Documentation**: Update README for any architectural changes

---

*Built with Context Engineering Framework v2.0.0 - Delivering reliable, scalable, and compliant GDPR contract analysis.*
=======
# Blackletter Systems - AI Contract Review

Simple, fast contract review using AI. Upload → Extract → Summarise → Show risks.

## Quick Start (Windows)

### Backend Setup

```powershell
cd blackletter\backend
python -m venv ..\.venv
. ..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
setx OPENAI_API_KEY "<YOUR_KEY>"
uvicorn main:app --reload --port 8000
```

### Frontend Setup

<<<<<<< Updated upstream
- [Implementation Plan](docs/Implementation.md)
- [Project Structure](docs/project_structure.md)
- [UI/UX Design](docs/UI_UX_doc.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Copilot Instructions](docs/COPILOT_INSTRUCTIONS.md)
- [Context Engineering Workflow](docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md)
=======
```powershell
cd frontend
npm install
setx NEXT_PUBLIC_API_URL "http://localhost:8000"
npm run dev
```
>>>>>>> Stashed changes

## System Constraints

- Max file size: 10MB
- File type: PDF only
- Text limit: ~6,000 chars (for LLM processing)

## How We Build

✅ Ship the smallest slice: upload → extract → summarise → show.
✅ Windows-only instructions.
✅ Clear errors, simple UI, one happy path.
❌ Don't add auth/payments yet.
❌ Don't attempt OCR or RAG today.
❌ Don't over-engineer file storage.

## Testing

Use the provided `scripts/test_upload.http` with VS Code REST Client extension to test the API directly:

```http
POST http://localhost:8000/api/review
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.pdf"
Content-Type: application/pdf

< ./test.pdf
------WebKitFormBoundary--
```

## Next Steps

1. Add clause heuristics (termination, assignment, rent review, liability)
2. Redline docx export
3. Add playbook YAML and score risks against it
4. Logging + basic analytics
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
