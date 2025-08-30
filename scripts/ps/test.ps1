Write-Host "== Backend unit tests =="
Push-Location apps\api
py -3.11 -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt pytest requests
pytest -q
deactivate; Pop-Location

Write-Host "`n== Frontend E2E =="
Push-Location apps\web
npm i; npx playwright install --with-deps
npx playwright test
Pop-Location

Write-Host "`n== Smoke Check =="
Invoke-RestMethod https://bmad-backletter.onrender.com/health
