# Development Workflow

## Local Setup

Developers will run tools/windows/dev.ps1, which uses Docker Compose to spin up all necessary services (api, web, worker, db, redis).

## Environment Variables

All secrets and configurations will be managed through .env files, with .env.example serving as a template.

## CI/CD

The ci.yml workflow in GitHub Actions will run on every pull request, executing linters and test suites for both the frontend and backend.
