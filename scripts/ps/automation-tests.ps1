# Windows one-liner runner
$ErrorActionPreference = "Stop"
pnpm install --frozen-lockfile
pnpm run test
