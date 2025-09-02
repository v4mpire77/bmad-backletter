# Epic E0: Platform & Security Baseline

**Epic Goal:** Establish foundational infrastructure, security protocols, and developer workflows.

## Story E0.1: Repository Scaffold & Source Tree

- Create monorepo with `apps/web` (Next.js) and `apps/api` (FastAPI).
- Include `docs/`, `tools/windows/`, and `core-config.yaml`.

## Story E0.2: Windows Developer Environment

- PowerShell runbooks (`dev.ps1`, `test.ps1`) that spin up docker-compose and run tests.

## Story E0.3: Coding Standards & Linters

- Configure ruff, black, ESLint, and Prettier; add CI job to enforce.
