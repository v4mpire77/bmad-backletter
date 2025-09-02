$env:NODE_ENV = "development"
$env:PYTHONUNBUFFERED = "1"
$env:SECRET_KEY = (powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\Generate-Secret.ps1")

# Local Supabase defaults
$env:SUPABASE_URL = "http://localhost:54321"
$env:SUPABASE_ANON_KEY = "dev-anon-key"
$env:SUPABASE_SERVICE_ROLE_KEY = "dev-service-key"

# API
$env:API_INTERNAL_URL = "http://localhost:8000"
$env:NEXT_PUBLIC_API_URL = $env:API_INTERNAL_URL

# Frontend public
$env:NEXT_PUBLIC_SUPABASE_URL = $env:SUPABASE_URL
$env:NEXT_PUBLIC_SUPABASE_ANON_KEY = $env:SUPABASE_ANON_KEY

Write-Host "Local env set. Backend: $env:API_INTERNAL_URL; Supabase: $env:SUPABASE_URL"
