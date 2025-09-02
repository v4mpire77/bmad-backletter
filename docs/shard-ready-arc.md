 # Blackletter Systems — Fullstack Architecture

**Owner:** Winston (Architect)

**Mode:** Windows‑first • Rules‑first • Evidence‑first • LLM OFF by default

**Repo Model:** Monorepo

**Version:** 2.0 (Consolidated)

**Date:** 2025-09-01

## 0. Foundation & Scope

Starter/Codebase: This architecture is designed for a greenfield project but will be implemented within a pre-defined monorepo structure as specified in the project's build guides.

Goal: To translate the validated PRD and UX Specification into a production-ready, scalable, and low-cost architecture with GDPR-by-design.

Audiences: Engineering, Security, Product, Operations.

## 1. System Overview

Style: The architecture is a modern full-stack application consisting of a core API "monolith" (FastAPI), background workers (Celery with Redis), and a server-side rendered web application (Next.js).

### Principles

- Deterministic First: The core analysis engine relies on verifiable rulepacks, lexicons, and regex. LLM features are disabled by default.
- Evidence Everywhere: Every finding is traceable to a specific text snippet, ensuring auditability.
- Windows-Friendly DX: All development and setup scripts are designed to run seamlessly on Windows.
- Cost Minimal: The technology stack is chosen to leverage generous free tiers and low-cost managed services.

### High‑level Services

- Web App: A Next.js 14 (App Router) application for all user interactions, including uploads, dashboards, and the evidence viewer.
- API: A FastAPI service that handles contract ingestion, job orchestration, and serves findings to the frontend.
- Worker: A Celery-based worker process for handling long-running, asynchronous tasks like text extraction and rule-based analysis.
- Database & Cache: PostgreSQL for persistent storage and Redis as a message broker for Celery and for caching.
- Storage: An S3-compatible object storage for uploaded documents and generated reports.

## 2. Environments & Deployment

Environments: local (Windows), staging, prod.

### Local (Windows)

- Docker Desktop + Compose: A docker-compose.local.yml will manage containers for the api, web app, worker, db (Postgres), and redis.
- PowerShell Scripts: A suite of scripts in tools/windows/ will handle bootstrapping, running, testing, and linting the entire application.

### Production (Recommended)

- Web (Next.js): Vercel, for its seamless integration with Next.js and global CDN.
- API / Worker: Render, using a Web Service for the API and a Background Worker for Celery.
- Database: A managed Postgres service like Neon, Supabase, or Render's offering.
- Redis: Upstash for its serverless, low-cost Redis instances.
- Storage: An S3-compatible service like Cloudflare R2 or Supabase Storage.
- CI/CD: GitHub Actions will be used to run tests on every pull request and deploy to staging/production environments upon merge to the respective branches.

## 3. Tech Stack

This table represents the definitive technology stack for the project. All development must adhere to these choices and versions.

| Category | Technology | Version | Purpose & Rationale |
|---|---:|---:|---|
| Frontend Language | TypeScript | 5.4.x | Provides strong typing for a more robust and maintainable frontend codebase. |
| Frontend Framework | Next.js | 14.2.x | Enables server-side rendering for fast initial page loads and a great developer experience with the App Router. |
| UI Library | React | 18.2.x | The industry standard for building dynamic and responsive user interfaces. |
| UI Components | shadcn/ui | latest | A collection of accessible and composable components that accelerate UI development. |
| Styling | Tailwind CSS | 3.4.x | A utility-first CSS framework for rapid and consistent styling. |
| Backend Language | Python | 3.11 | A modern, stable version of Python with excellent support for web development and data processing. |
| Backend Framework | FastAPI | 0.111.x | A high-performance Python framework for building APIs with automatic validation and documentation. |
| ORM | SQLAlchemy | 2.0.x | A powerful and flexible ORM for interacting with the PostgreSQL database. |
| Database Migrations | Alembic | latest | Manages database schema changes in a version-controlled and repeatable manner. |
| Async Tasks | Celery | 5.3.x | A robust distributed task queue for handling asynchronous operations like document processing. |
| Database | PostgreSQL | 15 | A reliable, open-source relational database for storing application data. |
| Cache / Broker | Redis | 7.x | An in-memory data store used as a message broker for Celery and for caching. |
| File Storage | S3-Compatible | - | Provides a scalable and cost-effective solution for storing user-uploaded files. |
| Frontend Testing | Vitest / RTL | latest | A fast and modern testing framework for React components, combined with React Testing Library. |
| E2E Testing | Playwright | latest | A reliable framework for end-to-end testing of the full user journey. |
| Backend Testing | Pytest | latest | The standard for testing Python applications, known for its simplicity and powerful features. |
| CI/CD | GitHub Actions | - | Automates the build, test, and deployment pipeline directly from the repository. |

## 4. Data Models

The following TypeScript interfaces define the core data models. These types can be shared between the frontend and backend to ensure consistency.

```ts
// In packages/shared/src/types/index.ts

export interface Document {
  id: string; // UUID
  org_id: string;
  filename: string;
  mime_type: string;
  size_bytes: number;
  storage_uri: string;
  sha256: string;
  status: 'uploaded' | 'processing' | 'completed' | 'error';
  created_at: string; // ISO 8601
}

export interface Job {
  id: string; // UUID
  doc_id: string;
  status: 'queued' | 'running' | 'done' | 'error';
  error_message?: string;
  created_at: string;
}

export interface Sentence {
  id: string;
  doc_id: string;
  page_number: number;
  text: string;
  start_char: number;
  end_char: number;
}

export interface Finding {
  id: string;
  doc_id: string;
  rule_id: string; // e.g., "art28-3-a"
  verdict: 'pass' | 'weak' | 'missing' | 'needs_review';
  snippet: string; // The evidence window text
  location: {
    page: number;
    start_char: number;
    end_char: number;
  };
}
```

## 5. API Specification

The backend will expose a RESTful API. The initial endpoints for Sprint 1 are defined below in OpenAPI 3.0 format.

```yaml
openapi: 3.0.0
info:
  title: Blackletter API
  version: v1.0
servers:
  - url: /v1
    description: Version 1 API
paths:
  /docs/upload:
    post:
      summary: Upload a contract for analysis
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        '202':
          description: Accepted for processing
          content:
            application/json:
              schema:
                type: object
                properties:
                  job_id:
                    type: string
  /jobs/{job_id}:
    get:
      summary: Get the status of a processing job
      parameters:
        - name: job_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Job status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Job'
  /docs/{doc_id}/findings:
    get:
      summary: Get the analysis findings for a document
      parameters:
        - name: doc_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: List of findings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Finding'
  /exports/{doc_id}.html:
    get:
      summary: Export the findings as an HTML report
      parameters:
        - name: doc_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: HTML report
          content:
            text/html:
              schema:
                type: string
components:
  schemas:
    Job:
      type: object
      properties:
        id: { type: string }
        doc_id: { type: string }
        status: { type: string, enum: [queued, running, done, error] }
        error_message: { type: string }
    Finding:
      type: object
      properties:
        id: { type: string }
        rule_id: { type: string }
        verdict: { type: string, enum: [pass, weak, missing, needs_review] }
        snippet: { type: string }
        location:
          type: object
          properties:
            page: { type: integer }
            start_char: { type: integer }
            end_char: { type: integer }
```

## 6. Unified Project Structure

The project will be organized as a monorepo to facilitate code sharing and streamlined development.

```
/blackletter
├── .github/
│   └── workflows/
│       └── ci.yml
├── apps/
│   ├── web/            # Next.js 14 Frontend
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── package.json
│   └── api/            # FastAPI Backend
│       ├── blackletter_api/
│       │   ├── routers/
│       │   ├── services/
│       │   ├── models/
│       │   └── main.py
│       ├── tests/
│       └── requirements.txt
├── packages/
│   └── shared/         # Shared TypeScript types and utilities
├── tools/
│   └── windows/
│       ├── dev.ps1
│       └── test.ps1
├── docker-compose.local.yml
└── core-config.yaml
```

## 7. Development Workflow

Local Setup: Developers will run tools/windows/dev.ps1, which uses Docker Compose to spin up all necessary services (api, web, worker, db, redis).

Environment Variables: All secrets and configurations will be managed through .env files, with .env.example serving as a template.

CI/CD: The ci.yml workflow in GitHub Actions will run on every pull request, executing linters and test suites for both the frontend and backend.

## 8. Testing Strategy

- Backend Unit Tests (Pytest): Focus on the business logic within the services, particularly the rule engine's verdict logic and the text extraction/sentence splitting functions.
- Backend Integration Tests (Pytest): Test the API endpoints' interaction with the database and the full processing pipeline from file upload to finding persistence.
- Frontend Component Tests (Vitest/RTL): Test individual React components in isolation to verify rendering and user interactions.
- E2E Smoke Test (Playwright): A single, critical-path test that simulates the entire user journey: uploading a document, polling for completion, viewing the findings, opening the evidence drawer, and exporting the report.

## 9. Coding Standards

- Type Sharing: All data models and types shared between the frontend and backend will reside in the packages/shared directory.
- API Calls: The frontend will use a dedicated service layer for all API interactions; no direct fetch calls in components.
- Environment Variables: Access environment variables only through dedicated configuration modules, never directly via process.env.
- Error Handling: All API routes must use a standardized error handling middleware to ensure consistent error responses.
- Database Access: The backend will use the Repository Pattern; no direct ORM calls from the router/controller layer.
