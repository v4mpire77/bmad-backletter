# Blackletter - Technology Stack

This document provides a detailed overview of the technology stack for the Blackletter project, with justifications for each choice.

## 1. Overview

The technology stack is designed to be deterministic, explainable, and production-ready for the MVP. It prioritizes Windows-friendly development workflows, low cost, and a rules-first engine with LLM usage disabled by default.

## 2. Frontend

-   **Framework**: Next.js 14 (App Router)
-   **Language**: TypeScript 5.x
-   **Styling**: Tailwind CSS 3.x
-   **UI Components**: shadcn/ui utilizing Radix primitives
-   **Icons**: lucide-react
-   **Data Fetching**: React Query for managing server state

> Note: The current scaffold under `apps/web` uses Next.js 15, React 19, and Tailwind CSS 4. For fastest SM↔Dev iteration, we accept these in MVP and record the deviation. A follow-up ADR can decide whether to downshift to the pinned matrix or fully adopt the newer versions.

## 3. Backend

-   **Language**: Python 3.11+
-   **Framework**: FastAPI 0.11x with Uvicorn
-   **Document Extraction**: PyMuPDF (fitz) for PDF and python-docx/docx2python for DOCX
-   **Sentence Segmentation**: blingfire, chosen for being fast and Windows-friendly
-   **Optional OCR**: Tesseract via pytesseract (disabled by default)
-   **Database ORM**: SQLAlchemy 2.0.x
-   **Data Validation**: Pydantic 2.7.x

## 4. Storage & Infrastructure

-   **Development Database**: SQLite for simplicity and file-backed storage
-   **Cloud Database**: PostgreSQL (specifically via Supabase)
-   **File Storage**: Local filesystem in development; object storage (e.g., Supabase Storage) in the cloud
-   **Asynchronous Jobs**: FastAPI `BackgroundTasks` are used for the MVP, with a planned upgrade path to Celery with Redis for more durable queueing

## 5. Tooling & QA

-   **Backend Testing**: Pytest and pytest-asyncio
-   **Frontend Testing**: Vitest and Playwright
-   **Python Linting/Formatting**: Ruff and Black
-   **TypeScript Linting/Formatting**: ESLint and Prettier

## 6. Version Locking Strategy

-   A strict version pinning policy will be followed.
-   Exact versions for all packages will be recorded in `versions.lock.md` at the start of the project, in addition to standard lockfiles (`package-lock.json`, `requirements.txt`).

## 7. Trade-offs & Alternatives

-   **BackgroundTasks vs. Celery**: The project will start with the simpler `BackgroundTasks` for the MVP and feature-flag a move to Celery for its durable retries and parallelism in a later phase.
-   **SQLite vs. Postgres**: Development starts on SQLite for speed, while production will use Postgres for concurrency and scale. The transition will be managed by a repository layer and Alembic migrations.
-   **PDF Rendering**: Headless Chromium is the chosen method for generating PDF reports due to its consistent CSS handling, over alternatives like wkhtmltopdf which can have CSS quirks.
