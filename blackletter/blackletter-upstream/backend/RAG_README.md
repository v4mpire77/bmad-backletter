# RAG (Retrieval-Augmented Generation) System

This document describes the RAG system implementation for Blackletter Systems, which enhances contract analysis with advanced document retrieval and generation capabilities.

## Overview

The RAG system provides:
- **Document Storage**: Efficient storage of contract documents with automatic chunking
- **Semantic Search**: Advanced search capabilities using embeddings
- **Context-Aware Generation**: LLM responses based on retrieved document context
- **Compliance Analysis**: Automated compliance checking using RAG
- **Risk Assessment**: Enhanced risk analysis with document context

## Architecture

### Core Components

1. **Enhanced RAG Store** (`app/services/rag_store.py`)
   - ChromaDB integration for vector storage
   - In-memory fallback for development
   - Automatic text chunking with overlap
   - Metadata tracking

2. **LLM Adapter** (`app/core/llm_adapter.py`)
   - Embedding generation using sentence-transformers
   - OpenAI embeddings fallback
   - Context-aware response generation
   - Multi-provider support (OpenAI, Ollama)

3. **RAG Analyzer** (`app/services/rag_analyzer.py`)
   - Comprehensive contract analysis
   - Compliance checking
   - Risk assessment
   - Document comparison

4. **RAG Router** (`routers/rag.py`)
   - REST API endpoints for RAG operations
   - Document upload and processing
   - Query and search functionality
   - Batch operations

## Installation

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: Install ChromaDB for production
pip install chromadb
```

### Environment Variables

```bash
# LLM Configuration
LLM_PROVIDER=ollama  # or openai
DEFAULT_LLM=llama3.1:8b  # or gpt-4
OPENAI_API_KEY=your_openai_key  # if using OpenAI
OLLAMA_BASE_URL=http://localhost:11434  # if using Ollama

# RAG Configuration
CHROMA_PERSIST_DIR=./chroma_db  # ChromaDB storage directory
```

## API Endpoints

### Document Management

#### Upload Document
```http
POST /api/rag/upload
Content-Type: multipart/form-data

file: [PDF/TXT/DOCX file]
```

**Response:**
```json
{
  "doc_id": "uuid",
  "filename": "contract.pdf",
  "size": 1024000,
  "upload_time": "2024-01-01T12:00:00Z"
}
```

#### List Documents
```http
GET /api/rag/documents
```

#### Delete Document
```http
DELETE /api/rag/documents/{doc_id}
```

### Query and Search

#### Query Documents
```http
POST /api/rag/query
Content-Type: application/x-www-form-urlencoded

query=What are the payment terms?
doc_id=optional_doc_id
top_k=5
use_semantic_search=true
```

**Response:**
```json
{
  "answer": "Based on the contract...",
  "chunks": [
    {
      "id": "chunk_id",
      "text": "Payment shall be made...",
      "page": 3,
      "similarity_score": 0.85,
      "start_pos": 1200,
      "end_pos": 1400
    }
  ],
  "query": "What are the payment terms?",
  "total_chunks_retrieved": 3
}
```

#### Search Documents
```http
POST /api/rag/search
Content-Type: application/x-www-form-urlencoded

query=liability clause
doc_id=optional_doc_id
top_k=10
similarity_threshold=0.7
```

#### Batch Query
```http
POST /api/rag/batch-query
Content-Type: application/x-www-form-urlencoded

queries=["query1", "query2", "query3"]
doc_id=optional_doc_id
top_k=5
```

### Analysis and Reports

#### Get Document Chunks
```http
GET /api/rag/documents/{doc_id}/chunks
```

#### Get RAG Statistics
```http
GET /api/rag/stats
```

## Usage Examples

### Python Client Example

```python
import requests

# Upload a document
with open('contract.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/rag/upload',
        files={'file': f}
    )
doc_data = response.json()
doc_id = doc_data['doc_id']

# Query the document
query_response = requests.post(
    'http://localhost:8000/api/rag/query',
    data={
        'query': 'What are the termination conditions?',
        'doc_id': doc_id,
        'top_k': 5
    }
)
result = query_response.json()
print(result['answer'])
```

### JavaScript/TypeScript Example

```typescript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('/api/rag/upload', {
  method: 'POST',
  body: formData
});
const docData = await uploadResponse.json();

// Query document
const queryResponse = await fetch('/api/rag/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    query: 'What are the key obligations?',
    doc_id: docData.doc_id,
    top_k: '5'
  })
});
const result = await queryResponse.json();
```

## Advanced Features

### RAG Analyzer Integration

The RAG Analyzer provides enhanced contract analysis:

```python
from app.services.rag_analyzer import rag_analyzer

# Comprehensive analysis
analysis = await rag_analyzer.analyze_contract_with_rag(
    doc_id="contract_123",
    text=contract_text,
    metadata={"filename": "contract.pdf"}
)

# Query specific contract
result = await rag_analyzer.query_contract(
    doc_id="contract_123",
    query="What are the data protection obligations?",
    include_context=True
)

# Compare multiple contracts
comparison = await rag_analyzer.compare_contracts(
    doc_ids=["contract_1", "contract_2"],
    comparison_criteria=["payment terms", "liability clauses"]
)

# Generate summary report
report = await rag_analyzer.generate_summary_report("contract_123")
```

### Custom Embeddings

The system supports multiple embedding models:

1. **Sentence Transformers** (default): `all-MiniLM-L6-v2`
2. **OpenAI Embeddings**: `text-embedding-ada-002`
3. **Fallback**: Simple hash-based embeddings

### Vector Storage Options

1. **ChromaDB** (recommended for production)
   - Persistent storage
   - Advanced querying
   - Metadata filtering

2. **In-Memory Storage** (development)
   - Fast for small datasets
   - No persistence
   - Good for testing

## Configuration

### ChromaDB Setup

```python
# In rag_store.py
rag_store = EnhancedRAGStore(
    embedding_dim=384,  # all-MiniLM-L6-v2 dimension
    persist_directory="./chroma_db"
)
```

### Chunking Configuration

```python
# Custom chunking parameters
chunks = rag_store.chunk_text(
    text=document_text,
    doc_id="doc_123",
    chunk_size=1000,  # characters per chunk
    overlap=200       # overlap between chunks
)
```

## Performance Considerations

### Optimization Tips

1. **Chunk Size**: Balance between context and retrieval speed
   - Small chunks (500-800 chars): Better precision
   - Large chunks (1000-1500 chars): Better context

2. **Overlap**: Use 15-20% overlap for better context continuity

3. **Top-K**: Start with 5-10 for most queries

4. **Similarity Threshold**: Use 0.7-0.8 for quality filtering

### Scaling

- **ChromaDB**: Supports millions of documents
- **Embedding Caching**: Consider caching frequent queries
- **Batch Processing**: Use batch endpoints for multiple operations

## Troubleshooting

### Common Issues

1. **ChromaDB Connection Error**
   ```bash
   # Check if ChromaDB is running
   pip install chromadb
   python -c "import chromadb; print('ChromaDB available')"
   ```

2. **Embedding Model Loading**
   ```bash
   # Install sentence-transformers
   pip install sentence-transformers
   ```

3. **Memory Issues**
   - Reduce chunk size
   - Use ChromaDB instead of in-memory storage
   - Implement document cleanup

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check RAG store stats
stats = rag_store.get_stats()
print(stats)
```

## Security Considerations

1. **Document Privacy**: Ensure proper access controls
2. **API Security**: Implement authentication and rate limiting
3. **Data Retention**: Configure document deletion policies
4. **Embedding Security**: Consider encryption for sensitive documents

## Future Enhancements

1. **Multi-modal Support**: Images, tables, diagrams
2. **Real-time Updates**: Live document synchronization
3. **Advanced Filtering**: Date ranges, document types
4. **Collaborative Features**: Shared document spaces
5. **Custom Models**: Domain-specific embedding models

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests
3. Update documentation
4. Consider performance implications
5. Maintain backward compatibility

## License

This RAG system is part of Blackletter Systems and follows the same licensing terms.
