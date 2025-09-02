# ADR 0001: Repository Structure

## Status
Accepted

## Context
We maintain a monorepo with Next.js frontend and FastAPI backend. Documentation must live under `docs/` so code and docs evolve together and remain Windows-friendly.

## Decision
- Place canonical docs at `docs/prd.md`, `docs/architecture.md`, and `docs/ux.md`.
- Store ADRs in `docs/adr/` with numeric filenames.
- Use Windows-first scripts under `tools/windows/` for local development.

## Consequences
- Contributors find authoritative docs in one location.
- Windows developers have a consistent experience.
