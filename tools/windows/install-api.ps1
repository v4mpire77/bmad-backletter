param(
  [switch]$WithML
)

Write-Host ">>> Installing API deps (lean)..."
python -m pip install --upgrade pip
pip install -r requirements.txt

if ($WithML) {
  Write-Host ">>> Installing ML extras..."
  pip install -r requirements-ml.txt
}
