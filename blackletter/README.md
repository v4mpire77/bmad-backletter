# Blackletter – Render + Vercel + Supabase (Windows-first)

## Quickstart (Windows)
```powershell
# 1) Set local env
powershell -ExecutionPolicy Bypass -File .\infra\scripts\Set-Local-Env.ps1

# 2) Start Supabase local (optional)
npm i -g supabase
npx supabase start

# 3) Backend (new terminal)
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 4) Frontend (new terminal)
cd frontend
npm i
npm run dev
```

* Backend health: [http://localhost:8000/healthz](http://localhost:8000/healthz)
* Frontend health page: [http://localhost:3000/health](http://localhost:3000/health)
