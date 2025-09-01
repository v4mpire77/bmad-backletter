param(
    [Parameter(Mandatory=$true)][string]$Chunks,
    [Parameter(Mandatory=$true)][string]$Rules,
    [Parameter(Mandatory=$true)][string]$Out
)

$directory = Split-Path $Out -Parent
if (-not (Test-Path $directory)) {
    New-Item -ItemType Directory -Path $directory | Out-Null
}

python -m engine.cli --chunks $Chunks --rules $Rules --out $Out
