# Blackletter - Source Tree

This document details the source tree structure and module organization for the Blackletter project.

## 1. Root Directory Structure

```
bmad-backletter/
  apps/
    web/                     # Next.js 14 app
      app/
      components/
      lib/
      styles/
      public/
      package.json
      tsconfig.json
    api/                     # FastAPI service
      blackletter_api/
        main.py
        config.py
        routers/
        services/
        rules/
        models/
        tests/
      pyproject.toml
      requirements.txt
    docs/
      prd.md
      architecture.md
      prd/
      architecture/
      stories/
  .bmad-core/core-config.yaml   # Central config: LLM gate, caps, OCR toggle
  README.md
```

## 2. Frontend Structure (`apps/web/`)

-   **`app/`**: Contains the pages and layouts for the Next.js App Router.
-   **`components/`**: Houses reusable UI components (e.g., buttons, tables, drawers) built with shadcn/ui.
-   **`lib/`**: Includes utility functions and custom React Query hooks for data fetching.
-   **`styles/`**: Global styles and Tailwind CSS configuration.
-   **`public/`**: Static assets like images and fonts.

## 3. Backend Structure (`apps/api/`)

-   **`blackletter_api/`**: The main Python package for the API.
-   **`blackletter_api/main.py`**: The FastAPI application entry point.
-   **`blackletter_api/config.py`**: Handles loading environment variables and the `core-config.yaml` file.
-   **`blackletter_api/routers/`**: Contains API route handlers (e.g., `uploads.py`, `jobs.py`). Business logic should not be here.
-   **`blackletter_api/services/`**: Contains modules with core business logic (e.g., `extraction.py`, `detection.py`).
-   **`blackletter_api/rules/`**: Stores the YAML rulepacks and lexicons that drive the detection engine.
-   **`blackletter_api/models/`**: Defines data models, including Pydantic schemas for I/O (`schemas.py`) and SQLAlchemy ORM models (`entities.py`).
-   **`blackletter_api/tests/`**: Contains unit and integration tests for the backend.
