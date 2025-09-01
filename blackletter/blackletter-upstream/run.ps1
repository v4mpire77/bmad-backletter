# Start backend and frontend for local development
$backend = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "backend.main:app", "--reload", "--app-dir", "src" -PassThru
$frontend = Start-Process -FilePath "npm" -ArgumentList "run", "dev", "--prefix", "frontend" -PassThru
Wait-Process -Id $backend.Id, $frontend.Id
