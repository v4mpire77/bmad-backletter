param(
    [Parameter(Mandatory=$true)][string]$Fixtures,
    [Parameter(Mandatory=$true)][string]$Rules,
    [Parameter(Mandatory=$true)][string]$Out
)

Import-Module powershell-yaml

$expectationsPath = Join-Path $PSScriptRoot 'eval/expectations.yaml'
$expectations = Get-Content $expectationsPath | ConvertFrom-Yaml

$ruleFiles = Get-ChildItem -Path $Rules -Recurse -Filter *.yml
$rules = @()
foreach ($rf in $ruleFiles) {
    $r = Get-Content $rf.FullName | ConvertFrom-Yaml
    if ($r) {
        $r.ruleset = Split-Path $rf.DirectoryName -Leaf
        $rules += $r
    }
}

$stats = @{}

Get-ChildItem -Path $Fixtures -Filter *.txt | ForEach-Object {
    $file = $_
    $text = Get-Content $file.FullName -Raw
    $expected = $expectations[$file.Name]
    if (-not $expected) { $expected = @() }

    foreach ($r in $rules) {
        $set = $r.ruleset
        if (-not $stats.ContainsKey($set)) { $stats[$set] = @{tp=0; fp=0; fn=0} }

        $hit = $true
        foreach ($phrase in $r.logic.contains_text) {
            if ($text -notmatch [regex]::Escape($phrase)) { $hit = $false; break }
        }

        if ($hit) {
            if ($expected -contains $r.id) { $stats[$set].tp++ } else { $stats[$set].fp++ }
        } else {
            if ($expected -contains $r.id) { $stats[$set].fn++ }
        }
    }
}

$results = @{}
$sumTP=0;$sumFP=0;$sumFN=0
foreach ($set in $stats.Keys) {
    $tp=$stats[$set].tp; $fp=$stats[$set].fp; $fn=$stats[$set].fn
    $sumTP+=$tp; $sumFP+=$fp; $sumFN+=$fn
    $prec = if (($tp+$fp) -gt 0) { [math]::Round($tp/($tp+$fp),2) } else { 1 }
    $rec = if (($tp+$fn) -gt 0) { [math]::Round($tp/($tp+$fn),2) } else { 1 }
    $results[$set] = @{precision=$prec; recall=$rec}
    Write-Host "$set precision: $prec recall: $rec"
}
$overallPrec = if (($sumTP+$sumFP) -gt 0) { [math]::Round($sumTP/($sumTP+$sumFP),2) } else { 1 }
$overallRec = if (($sumTP+$sumFN) -gt 0) { [math]::Round($sumTP/($sumTP+$sumFN),2) } else { 1 }
Write-Host "overall precision: $overallPrec recall: $overallRec"

$badgeMessage = "p:$([math]::Round($overallPrec*100)) r:$([math]::Round($overallRec*100))"
$color = if ($overallPrec -ge 0.95 -and $overallRec -ge 0.95) { 'green' } else { 'orange' }

$final = @{results=$results; overall=@{precision=$overallPrec; recall=$overallRec}; schemaVersion=1; label='eval'; message=$badgeMessage; color=$color}
$final | ConvertTo-Json -Depth 5 | Set-Content $Out
