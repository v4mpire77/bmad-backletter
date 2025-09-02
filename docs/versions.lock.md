# Blackletter - Locked Versions

This document contains the exact versions of all dependencies used in the Blackletter project. This ensures deterministic builds and deployments.

## Frontend Dependencies (package.json)

```json
{
  "dependencies": {
    "next": "14.2.5",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "typescript": "5.5.4",
    "tailwindcss": "3.4.7",
    "shadcn/ui": "0.0.1-alpha.27",
    "@radix-ui/react-icons": "1.3.0",
    "lucide-react": "0.427.0",
    "@tanstack/react-query": "5.51.15"
  },
  "devDependencies": {
    "eslint": "8.57.0",
    "prettier": "3.3.3",
    "@types/node": "20.14.12",
    "@types/react": "18.3.3",
    "@types/react-dom": "18.3.0",
    "autoprefixer": "10.4.19",
    "postcss": "8.4.39",
    "vitest": "2.0.5",
    "playwright": "1.45.3"
  }
}
```

## Backend Dependencies (requirements.txt)

```txt
fastapi==0.111.0
uvicorn==0.30.1
PyMuPDF==1.24.7
python-docx==1.1.0
docx2python==2.6.1
blingfire==0.1.8
pytesseract==0.3.10
sqlalchemy==2.0.31
pydantic==2.8.2
pytest==8.3.2
pytest-asyncio==0.23.7
ruff==0.5.5
black==24.4.2
```

## Development Tools

- **Node.js**: 20.15.1
- **Python**: 3.11.9
- **npm**: 10.7.0

## Infrastructure

- **Docker**: 26.1.4
- **PostgreSQL**: 16.3
- **SQLite**: 3.45.3
- **Redis**: 7.2.5 (for future Celery implementation)

## Notes

1. These versions are locked and should not be changed without thorough testing.
2. Any version updates should go through the change management process.
3. Security patches should be applied promptly after validation.
4. This file should be updated whenever dependency versions are changed.