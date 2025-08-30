param([ValidateSet('local','vercel','render','all')][string]$target='local')

$DATABASE_URL='postgresql://postgres:BBpxIZ59p69WhZGG@db.idqiauohdecqidqyseve.supabase.co:5432/postgres?sslmode=require'
$OPENAI_PROVIDER='none'
$OCR_ENABLED='false'
$NEXT_PUBLIC_API_URL='https://bmad-backletter.onrender.com'
$NEXT_PUBLIC_SUPABASE_URL='https://idqiauohdecqidqyseve.supabase.co'
$NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY='sb_publishable__Gy8apgtJiA1-Uz3eu68gA_YP6gbhNr'

function Set-Local {
  setx DATABASE_URL "$DATABASE_URL"
  setx OPENAI_PROVIDER "$OPENAI_PROVIDER"
  setx OCR_ENABLED "$OCR_ENABLED"
  setx NEXT_PUBLIC_API_URL "$NEXT_PUBLIC_API_URL"
  setx NEXT_PUBLIC_SUPABASE_URL "$NEXT_PUBLIC_SUPABASE_URL"
  setx NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY "$NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY"
  Write-Host "Local env set. Restart terminal."
}

function Set-Vercel {
  Write-Host "Run in apps\\web with Vercel CLI:"
  Write-Host "  vercel env add NEXT_PUBLIC_API_URL production \"$NEXT_PUBLIC_API_URL\""
  Write-Host "  vercel env add NEXT_PUBLIC_API_URL preview \"$NEXT_PUBLIC_API_URL\""
  Write-Host "  vercel env add NEXT_PUBLIC_SUPABASE_URL production \"$NEXT_PUBLIC_SUPABASE_URL\""
  Write-Host "  vercel env add NEXT_PUBLIC_SUPABASE_URL preview \"$NEXT_PUBLIC_SUPABASE_URL\""
  Write-Host "  vercel env add NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY production \"$NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY\""
  Write-Host "  vercel env add NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY preview \"$NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY\""
}

function Set-Render {
  Write-Host "Render → bmad-backletter → Settings → Environment → add:"
  Write-Host "  DATABASE_URL=$DATABASE_URL"
  Write-Host "  OPENAI_PROVIDER=$OPENAI_PROVIDER"
  Write-Host "  OCR_ENABLED=$OCR_ENABLED"
}

switch ($target) {'local'{Set-Local};'vercel'{Set-Vercel};'render'{Set-Render};'all'{Set-Local;Set-Vercel;Set-Render}}
