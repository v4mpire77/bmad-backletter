param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 8001
)

# Start the RAG API
uvicorn rag.api:app --host $Host --port $Port --reload
