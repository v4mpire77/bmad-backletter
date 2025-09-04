# Unified Project Structure

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
