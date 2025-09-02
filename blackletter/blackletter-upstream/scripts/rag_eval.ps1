param(
    [int]$k = 5
)

$ErrorActionPreference = "Stop"
python rag/eval/evaluate.py --k $k
