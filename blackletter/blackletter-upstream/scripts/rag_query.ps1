param(
    [string]$Query = "What are DPA Art.28 controller obligations?"
)

python -c "import json,sys; from rag.query import retrieve; print(json.dumps(retrieve(sys.argv[1]), indent=2))" "$Query"
