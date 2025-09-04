# Tech Stack

This table represents the definitive technology stack for the project. All development must adhere to these choices and versions.

| Category | Technology | Version | Purpose & Rationale |
|----------|------------|---------|---------------------|
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
