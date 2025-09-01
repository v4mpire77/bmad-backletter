param(
    [Parameter(Mandatory=$true)][string]$Path,
    [Parameter(Mandatory=$true)][string]$Out
)

python -m apps.ingest.cli --path $Path --out $Out
