# Batch enhance all draft stories to meet Definition of Ready requirements
# Usage: .\tools\enhance_all_draft_stories.ps1

param(
    [switch]$WhatIf,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$StoryDir = Join-Path $ProjectRoot "docs\stories"

Write-Host "🔍 Finding all draft stories in $StoryDir..." -ForegroundColor Cyan

# Find all draft stories
$DraftStories = Get-ChildItem -Path $StoryDir -Filter "*.md" | Where-Object {
    $content = Get-Content $_.FullName -Raw
    $content -match "status:\s*draft"
}

if ($DraftStories.Count -eq 0) {
    Write-Host "✅ No draft stories found. All stories are ready!" -ForegroundColor Green
    exit 0
}

Write-Host "📋 Found $($DraftStories.Count) draft stories:" -ForegroundColor Yellow
$DraftStories | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "🚀 Enhancing draft stories..." -ForegroundColor Green

foreach ($story in $DraftStories) {
    Write-Host "🔧 Processing: $($story.Name)" -ForegroundColor Blue

    $enhancerScript = Join-Path $ScriptDir "story_enhancement_template.py"

    if (Test-Path $enhancerScript) {
        if ($WhatIf) {
            Write-Host "   [WhatIf] Would run: python $enhancerScript $($story.FullName)" -ForegroundColor Gray
        } else {
            try {
                & python $enhancerScript $story.FullName
                Write-Host "✅ Enhanced: $($story.Name)" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to enhance: $($story.Name) - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "❌ Enhancement script not found: $enhancerScript" -ForegroundColor Red
        exit 1
    }

    Write-Host ""
}

if (-not $WhatIf) {
    Write-Host "🎉 All draft stories have been enhanced!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review each enhanced story for accuracy" -ForegroundColor White
    Write-Host "  2. Customize technical specifications as needed" -ForegroundColor White
    Write-Host "  3. Verify file paths and dependencies are correct" -ForegroundColor White
    Write-Host "  4. Update story status to 'approved' when ready for development" -ForegroundColor White
}
