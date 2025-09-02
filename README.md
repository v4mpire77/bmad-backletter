# Blackletter Systems - Unified Repository

**One definitive path for GDPR compliance checking and contract analysis.**

This repository has been consolidated to provide a single, comprehensive development environment for the Blackletter GDPR compliance system.

## 🗺️ Repository Structure

Following the **shard map** approach with **16 epics** as the foundation:

```
blackletter/
├── docs/                          # 📚 Consolidated documentation (SHARDED)
│   ├── README.md                  # Context Engineering Framework
│   ├── SHARD_MAP.md              # Document index and reading order
│   ├── backlog-blackletter/      # 16 Epics (E0-E16) - MVP foundation
│   ├── prd/                      # Product Requirements Document  
│   ├── shard-ready-arc/          # Architecture specification
│   ├── architecture-blackletter/ # System architecture details
│   └── tests-blackletter/        # Testing and QA strategy
├── apps/                          # 🚀 Application code
│   ├── api/                      # FastAPI backend with comprehensive rules
│   └── web/                      # Next.js frontend
├── tools/                         # 🔧 Development tools and scripts
├── BMAD-METHOD-main/             # 📦 BMAD methodology framework
└── web-bundles/                  # 🤖 Agent configurations
```

## 🚀 Quick Start

1. **Read the Documentation** (recommended order):
   - Start: [`docs/README.md`](docs/README.md) - Context Engineering Framework
   - Overview: [`docs/SHARD_MAP.md`](docs/SHARD_MAP.md) - Navigation guide
   - Epics: [`docs/backlog-blackletter/`](docs/backlog-blackletter/) - 16 epics foundation
   - Architecture: [`docs/shard-ready-arc.md`](docs/shard-ready-arc.md) - System design

2. **Development Setup**:
   ```bash
   # Python API setup
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   
   # Run API
   cd apps/api && uvicorn blackletter_api.main:app --reload
   ```

3. **Project Rules**: See [`AGENTS.md`](AGENTS.md) for comprehensive agent guidelines

## 🎯 The 16 Epics Foundation

The MVP is organized around **16 epics** (E0-E16) in [`docs/backlog-blackletter/`](docs/backlog-blackletter/):

- **E0**: Platform & Security Baseline
- **E1**: Ingestion & Extraction  
- **E2**: GDPR Rule Engine & Detection
- **E3**: Findings & Report UI
- **E4**: Metrics, Logging & Observability
- **E5**: Templates, Clause Library & Interview Builder
- **E6**: Governance & Settings
- **E7**: Accounts, Auth & Roles
- **E8**: Evidence, Provenance & Review Controls
- **E9**: Export, Sharing & Presentation
- **E10**: Storage & Data Layer
- **E11**: Evaluation & QA Harness
- **E12**: Cost & Performance Controls
- **E13**: DevEx Tooling & Agent Flows
- **E14**: Integrations
- **E15**: Pricing, Plans & Billing
- **E16**: Token & Evidence Layer

## 🧩 Key Features

- **Context Engineering Framework**: Structured development with AI agents
- **Comprehensive Rules Engine**: GDPR, UK ICS, and property compliance rules
- **Shard-Ready Architecture**: Modular, scalable system design
- **16-Epic MVP Structure**: Complete product roadmap
- **Consolidated Documentation**: Single source of truth

## 📖 Documentation Shards

This repository follows a **sharded documentation** approach where each major area has dedicated, focused documentation:

- **PRD Shard**: Product requirements and user stories
- **Architecture Shard**: Technical system design
- **Backlog Shard**: Epic and story management (16 epics)
- **Testing Shard**: QA strategy and test plans

See [`docs/SHARD_MAP.md`](docs/SHARD_MAP.md) for the complete navigation guide.

---

**Generated**: 2025-09-02 | **Consolidated from**: Multiple upstream sources  
**Framework**: Context Engineering with 16 Epic Foundation