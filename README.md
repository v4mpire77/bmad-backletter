# Blackletter - GDPR Processor Obligations Checker

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Next.js Version](https://img.shields.io/badge/next.js-14%2B-black.svg)](https://nextjs.org/)

Blackletter is a GDPR Processor Obligations Checker designed to automate the review of vendor contracts against the eight obligations outlined in Article 28(3) of the GDPR. The tool provides deterministic, explainable checks with pinpoint citations and clear rationale for each finding.

## Features

- **Deterministic Analysis**: Rule-based engine with clear, explainable decisions
- **GDPR Compliance**: Specialized in Article 28(3) compliance checks
- **Evidence-First Approach**: Every finding includes cited evidence and rationale
- **Fast Processing**: Sub-60 second processing time for most contracts
- **Cost-Effective**: Significantly lower cost than manual legal review
- **Exportable Reports**: PDF/HTML reports suitable for sharing with stakeholders

## Technology Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript 5.x**
- **Tailwind CSS 3.x**
- **shadcn/ui** with Radix primitives
- **React Query** for data fetching

### Backend
- **Python 3.11+**
- **FastAPI 0.11x**
- **PyMuPDF** for PDF processing
- **blingfire** for sentence segmentation
- **SQLAlchemy 2.0.x** for ORM

### Infrastructure
- **SQLite** for development
- **PostgreSQL** for production
- **FastAPI BackgroundTasks** for async processing

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/blackletter.git
   cd blackletter
   ```

2. Install frontend dependencies:
   ```bash
   cd apps/web
   npm install
   ```

3. Install backend dependencies:
   ```bash
   cd ../api
   pip install -r requirements.txt
   ```

4. Start the development servers:
   ```bash
   # In apps/web
   npm run dev
   
   # In apps/api
   uvicorn blackletter_api.main:app --reload
   ```

## Documentation

- [Product Requirements Document](docs/prd.md)
- [Architecture Overview](docs/architecture/source_tree.md)
- [Technology Stack](docs/architecture/tech_stack.md)
- [API Contracts](docs/architecture/api_contracts.md)
- [Coding Standards](docs/architecture/coding_standards.md)
- [Security Architecture](docs/architecture/security.md)
- [Operational Architecture](docs/architecture/operations.md)

## Contributing

We welcome contributions to Blackletter! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on GitHub or contact our team at support@blackletter.example.com.