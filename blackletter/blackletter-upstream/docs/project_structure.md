# Project Structure

## Root Directory

```
blackletter-systems/
├── frontend/                 # Next.js frontend application
├── backend/                  # FastAPI backend application
├── docs/                     # Project documentation
├── scripts/                  # Utility scripts and deployment
├── tests/                    # Test files and fixtures
├── .github/                  # GitHub configuration
├── .gitignore               # Git ignore rules
├── README.md                # Project overview
├── LICENSE                  # Project license
├── render.yaml              # Render deployment configuration
└── docker-compose.yml       # Docker development setup
```

## Frontend Structure

```
frontend/
├── app/                     # Next.js 14 app directory
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout component
│   ├── page.tsx             # Home page
│   ├── dashboard/           # Dashboard pages
│   │   ├── page.tsx         # Main dashboard
│   │   └── analysis/        # Analysis results
│   ├── upload/              # Document upload pages
│   │   └── page.tsx         # Upload interface
│   └── api/                 # API routes (if needed)
├── components/              # Reusable React components
│   ├── ui/                  # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── table.tsx
│   │   └── ...
│   ├── blackletter-app.tsx  # Main app component
│   ├── navigation.tsx       # Navigation component
│   ├── rag-interface.tsx    # RAG system interface
│   └── vague-terms-finder.tsx # Vague terms detection UI
├── lib/                     # Utility libraries
│   ├── utils.ts             # General utilities
│   └── api.ts               # API client functions
├── types/                   # TypeScript type definitions
│   ├── gdprRules.ts         # GDPR rule types
│   └── api.ts               # API response types
├── public/                  # Static assets
│   ├── images/              # Image files
│   └── icons/               # Icon files
├── styles/                  # Additional stylesheets
├── package.json             # Node.js dependencies
├── package-lock.json        # Locked dependencies
├── tsconfig.json            # TypeScript configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── next.config.js           # Next.js configuration
└── components.json          # shadcn/ui configuration
```

## Backend Structure

```
backend/
├── app/                     # Main application package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── core/                # Core application modules
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database connection
│   │   ├── security.py      # Authentication and security
│   │   ├── llm_adapter.py   # LLM integration
│   │   ├── nlp_engine.py    # NLP processing engine
│   │   └── ocr.py           # OCR processing
│   ├── models/              # Data models and schemas
│   │   ├── __init__.py
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── findings.py      # Analysis findings models
│   │   └── rules.py         # Compliance rules models
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── contracts.py     # Contract analysis endpoints
│   │   ├── dashboard.py     # Dashboard data endpoints
│   │   ├── rag.py           # RAG system endpoints
│   │   └── nlp_router.py    # NLP analysis endpoints
│   ├── services/            # Business logic services
│   │   ├── __init__.py
│   │   ├── corpus_gatherer.py    # Corpus collection service
│   │   ├── gemini_judge.py       # Gemini AI integration
│   │   ├── rag_analyzer.py       # RAG analysis service
│   │   ├── rag_store.py          # Vector store management
│   │   ├── rules_validator.py    # Compliance validation
│   │   └── vague_detector.py     # Vague terms detection
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── file_handlers.py # File processing utilities
│       └── validators.py    # Data validation utilities
├── rules/                   # Compliance rules and configurations
│   ├── __init__.py
│   ├── gdpr_rules.json      # GDPR compliance rules
│   ├── vague_terms.json     # Vague terms definitions
│   └── property/            # Property-specific rules
│       ├── aml_kyc_reference.yml
│       └── gdpr_dpa_clause.yml
├── scripts/                 # Utility scripts
│   ├── nlp_cli.py           # NLP command-line interface
│   └── validate_rules.py    # Rules validation script
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_nlp_system.py   # NLP system tests
│   ├── test_rag.py          # RAG system tests
│   ├── test_vague_terms.py  # Vague terms tests
│   └── fixtures/            # Test data and fixtures
│       ├── convert_to_pdf.py
│       ├── uk_commercial_lease.pdf
│       ├── uk_commercial_lease.txt
│       ├── uk_employment_contract.pdf
│       ├── uk_employment_contract.txt
│       ├── uk_nda.pdf
│       └── uk_nda.txt
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile              # Docker container configuration
├── .env.example            # Environment variables template
└── README.md               # Backend-specific documentation
```

## Documentation Structure

```
docs/
├── Implementation.md        # Main implementation plan
├── project_structure.md     # This file - project organization
├── UI_UX_doc.md            # UI/UX design specifications
├── Bug_tracking.md         # Bug tracking and resolution
├── API_DOCUMENTATION.md    # API reference documentation
├── ARCHITECTURE.md         # System architecture overview
├── DEPLOYMENT.md           # Deployment instructions
├── SECURITY.md             # Security guidelines
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md            # Version history
├── COPILOT_INSTRUCTIONS.md # Development agent instructions
└── assets/                 # Documentation assets
    ├── images/             # Documentation images
    └── diagrams/           # Architecture diagrams
```

## Configuration Files

### Root Level Configuration
- `.gitignore` - Git ignore patterns
- `.env` - Environment variables (not in git)
- `.env.example` - Environment variables template
- `docker-compose.yml` - Multi-container Docker setup
- `render.yaml` - Render deployment configuration

### Frontend Configuration
- `package.json` - Node.js dependencies and scripts
- `tsconfig.json` - TypeScript compiler options
- `tailwind.config.js` - Tailwind CSS configuration
- `next.config.js` - Next.js framework configuration
- `components.json` - shadcn/ui component configuration

### Backend Configuration
- `requirements.txt` - Python package dependencies
- `requirements-dev.txt` - Development dependencies
- `Dockerfile` - Docker container specification
- `pyproject.toml` - Python project configuration (if using modern Python)

## Asset Organization

### Frontend Assets
```
frontend/public/
├── images/                  # Static images
│   ├── logo.png            # Application logo
│   └── icons/              # Icon files
├── fonts/                  # Custom fonts
└── favicon.ico             # Browser favicon
```

### Backend Assets
```
backend/assets/
├── models/                 # Pre-trained models
├── templates/              # Document templates
└── static/                 # Static files served by FastAPI
```

## Build and Deployment Structure

### Development Environment
```
.venv/                      # Python virtual environment
node_modules/               # Node.js dependencies
dist/                       # Build output (if applicable)
```

### Production Deployment
```
deployment/
├── docker/                 # Docker deployment files
├── scripts/                # Deployment scripts
│   ├── deploy.sh           # Linux deployment script
│   └── deploy.bat          # Windows deployment script
└── configs/                # Production configurations
```

## Environment-Specific Configurations

### Development
- Local database connections
- Debug logging enabled
- Hot reloading enabled
- Mock external services

### Staging
- Staging database
- Limited external API access
- Performance monitoring
- Security testing

### Production
- Production database
- Full external API access
- Comprehensive monitoring
- Security hardening
- CDN integration

## Module/Component Hierarchy

### Frontend Component Hierarchy
```
App (Root)
├── Navigation
├── Dashboard
│   ├── AnalysisResults
│   ├── DocumentUpload
│   └── ComplianceCheck
├── RAGInterface
│   ├── DocumentProcessor
│   ├── SearchResults
│   └── ContextViewer
└── VagueTermsFinder
    ├── TermsList
    ├── AnalysisView
    └── Recommendations
```

### Backend Service Hierarchy
```
FastAPI App
├── Core Services
│   ├── NLPEngine
│   ├── OCRProcessor
│   └── LLMAdapter
├── Business Services
│   ├── ContractAnalyzer
│   ├── ComplianceValidator
│   ├── RAGAnalyzer
│   └── CorpusGatherer
└── API Routes
    ├── Contracts
    ├── Dashboard
    ├── RAG
    └── NLP
```

## File Naming Conventions

### Frontend
- Components: PascalCase (e.g., `DocumentUpload.tsx`)
- Utilities: camelCase (e.g., `apiUtils.ts`)
- Constants: UPPER_SNAKE_CASE (e.g., `API_ENDPOINTS.ts`)
- Types: PascalCase (e.g., `ContractTypes.ts`)

### Backend
- Modules: snake_case (e.g., `nlp_engine.py`)
- Classes: PascalCase (e.g., `ContractAnalyzer`)
- Functions: snake_case (e.g., `process_document`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`)

## Documentation Placement

- **API Documentation**: `docs/API_DOCUMENTATION.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Implementation Plan**: `docs/Implementation.md`
- **Project Structure**: `docs/project_structure.md`
- **UI/UX Design**: `docs/UI_UX_doc.md`
- **Deployment**: `docs/DEPLOYMENT.md`
- **Security**: `docs/SECURITY.md`
- **Contributing**: `docs/CONTRIBUTING.md`
- **Changelog**: `docs/CHANGELOG.md`

This structure ensures a clean, maintainable, and scalable codebase that follows industry best practices and supports the Context Engineering framework requirements.
