Set-Location apps\web
corepack enable
corepack prepare pnpm@latest --activate
pnpm i
$env:NEXT_PUBLIC_API_URL = $env:NEXT_PUBLIC_API_URL ? $env:NEXT_PUBLIC_API_URL : "http://127.0.0.1:8000"
pnpm dev
