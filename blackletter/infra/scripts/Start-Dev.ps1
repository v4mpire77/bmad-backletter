Start-Process powershell -ArgumentList "-NoExit","-Command","cd backend; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; uvicorn app.main:app --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit","-Command","cd frontend; npm i; npm run dev"
