# Automated Merge Conflict Resolution Script
# Resolves conflicts by keeping HEAD (newer) content

Write-Host \"Starting automated merge conflict resolution...\" -ForegroundColor Cyan

# Get all files with merge conflict markers
$conflictFiles = Get-ChildItem -Recurse -Include *.* | Where-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $content -and ($content -match '<<<<<<<|=======|>>>>>>>')
}

Write-Host \"Found $($conflictFiles.Count) files with merge conflicts\" -ForegroundColor Yellow

foreach ($file in $conflictFiles) {
    Write-Host \"Processing: $($file.FullName)\" -ForegroundColor White
    
    try {
        # Read file content
        $content = Get-Content $file.FullName -Raw
        
        # Remove conflict markers and keep HEAD content
        # Pattern: <<<<<<< HEAD\n(content)\n=======\n(other content)\n>>>>>>> hash
        $resolved = $content -replace '(?s)<<<<<<< HEAD\\r?\n(.*?)\\r?\n=======\\r?\n.*?\\r?\n>>>>>>> [^\\r\n]*', '$1'
        
        # Handle remaining orphaned markers
        $resolved = $resolved -replace '<<<<<<< HEAD\\r?\n', ''
        $resolved = $resolved -replace '=======\\r?\n', ''
        $resolved = $resolved -replace '>>>>>>> [^\\r\n]*\\r?\n?', ''
        
        # Write resolved content back
        Set-Content -Path $file.FullName -Value $resolved -NoNewline
        
        Write-Host \"  Resolved: $($file.Name)\" -ForegroundColor Green
    }
    catch {
        Write-Host \"  Error processing $($file.Name): $($_.Exception.Message)\" -ForegroundColor Red
    }
}

Write-Host \"Merge conflict resolution completed!\" -ForegroundColor Green

# Verify no conflicts remain
$remainingConflicts = Get-ChildItem -Recurse -Include *.* | Where-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $content -and ($content -match '<<<<<<<|=======|>>>>>>>')
}

if ($remainingConflicts.Count -eq 0) {
    Write-Host \"All merge conflicts resolved successfully!\" -ForegroundColor Green
} else {
    Write-Host \"Warning: $($remainingConflicts.Count) files still have conflicts\" -ForegroundColor Yellow
    $remainingConflicts | ForEach-Object { Write-Host \"  - $($_.FullName)\" }
}