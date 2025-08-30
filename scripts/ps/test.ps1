$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "."
python -m pytest apps/api/blackletter_api/tests -q
