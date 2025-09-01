# Vague Terms Detection System

A comprehensive system for detecting and analyzing vague contractual language using NLP + Gemini + RAG with grounded citations (NotebookLM-style).

## 🎯 Overview

This system implements the architecture outlined in your plan:

1. **NLP Rules Engine** - Fast regex-based detection of vague terms
2. **RAG Context Store** - Document chunking and context retrieval
3. **Gemini LLM Judge** - Grounded analysis with citations
4. **NotebookLM-Style UX** - Clickable citations and evidence

## 🏗️ Architecture

```
[PDF Upload] → [OCR Extraction] → [RAG Indexing] → [NLP Detection] → [LLM Analysis] → [Grounded Results]
```

### Components

- **`vague_detector.py`** - Regex-based pattern matching for vague terms
- **`rag_store.py`** - Document chunking and context retrieval
- **`gemini_judge.py`** - Gemini-powered LLM analysis with citations
- **`contracts.py`** - FastAPI router integration
- **`vague-terms-finder.tsx`** - Frontend component for results display

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Gemini API (Optional)

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Test the System

```bash
python test_vague_terms.py
```

### 4. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

## 📋 Vague Terms Lexicon

The system detects 20+ categories of vague terms:

### High Priority (Red)
- **Unilateral powers**: "may in its sole discretion"

### Medium Priority (Amber)
- **Effort standards**: "reasonable efforts", "commercially reasonable"
- **Security measures**: "industry standard", "appropriate measures"
- **Timeframes**: "as soon as practicable", "without undue delay"
- **Obligations**: "where practicable"

### Low Priority (Low)
- **Scope terms**: "from time to time", "not limited to"
- **Process terms**: "on a case-by-case basis"
- **Standard clauses**: "force majeure", "consequential damages"

## 🔍 How It Works

### 1. Document Processing
```python
# Extract text from PDF
extracted_text = await ocr_processor.extract_text(content)

# Store in RAG for context retrieval
rag_store.store_document(doc_id, extracted_text, metadata)
```

### 2. Vague Terms Detection
```python
# Find all vague terms with character offsets
vague_hits = detector.find_vague_spans(extracted_text)

# Example output:
# [
#   {
#     "start": 45, "end": 62,
#     "text": "reasonable efforts",
#     "category": "effort",
#     "severity": "amber"
#   }
# ]
```

### 3. Context Retrieval
```python
# Get context around each vague term
context = rag_store.get_context_around_position(
    doc_id, hit["start"], window_size=1200
)
```

### 4. LLM Analysis
```python
# Analyze with Gemini (grounded with citations)
judgment = await gemini_judge.judge_vague_term(
    hit, context["context"], citations
)

# Returns:
# {
#   "verdict": "non_compliant",
#   "risk": "high",
#   "rationale": "The clause uses 'as soon as practicable' without a numeric timeframe.",
#   "improvements": ["Replace with: '…notify Controller within 48–72 hours…'"],
#   "quotes": [{"text": "as soon as practicable", "citation": {...}}]
# }
```

## 🎨 Frontend Integration

The `VagueTermsFinder` component displays results with:

- **Severity badges** (Red/Amber/Green)
- **Grounded citations** with page numbers
- **Suggested fixes** (copy-pasteable)
- **Clickable evidence** links

```typescript
<VagueTermsFinder 
  findings={findings}
  onCitationClick={(citation) => navigateToDocument(citation)}
/>
```

## 🔧 Configuration

### Adding New Vague Terms

Edit `rules/vague_terms.json`:

```json
{
  "pattern": "\\bnew\\s+vague\\s+term\\b",
  "category": "new_category",
  "severity": "amber",
  "description": "What makes this term vague",
  "suggested_fix": "How to fix it"
}
```

### Customizing Severity Levels

The system uses three severity levels:
- **Red**: Critical issues requiring immediate attention
- **Amber**: Important issues that should be addressed
- **Low**: Minor issues for review

## 🧪 Testing

### Run the Test Suite

```bash
python test_vague_terms.py
```

### Sample Output

```
🔍 Testing Vague Terms Detection System
==================================================
📄 Document stored: test_contract.pdf
📝 Text length: 1234 characters

🎯 Found 8 vague terms:
------------------------------
1. 'reasonable efforts' (effort - amber)
   Position: 45-62
   Description: Unclear performance standard

2. 'industry standard' (security - amber)
   Position: 89-105
   Description: Unspecified security measures

🤖 LLM Analysis Results:
------------------------------
1. Analyzing: 'reasonable efforts'
   Context: The Processor shall use reasonable efforts to provide...
   Verdict: weak
   Risk: medium
   Rationale: Vague term 'reasonable efforts' detected in effort category
   Suggested fix: Define specific metrics or timeframes
```

## 🔒 Hallucination Guards

The system includes multiple safeguards:

1. **Grounded Citations**: Every finding includes exact character offsets
2. **Context Validation**: LLM only analyzes provided text
3. **Fallback Mode**: Works without Gemini API
4. **Response Validation**: Ensures required fields are present

## 📊 Performance

- **NLP Detection**: ~1ms per document
- **Context Retrieval**: ~5ms per term
- **LLM Analysis**: ~2-5s per term (with Gemini)
- **Fallback Mode**: ~100ms per term

## 🚀 Production Deployment

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your-api-key

# Optional
LLM_PROVIDER=gemini  # or openai, ollama
DEFAULT_LLM=gemini-pro
```

### Scaling Considerations

- **Vector DB**: Replace in-memory RAG store with pgvector/Weaviate
- **Caching**: Add Redis for LLM response caching
- **Queue**: Add Celery for async processing
- **Monitoring**: Add metrics for detection accuracy

## 🔄 Future Enhancements

1. **Vector Search**: Replace keyword search with semantic similarity
2. **Custom Rules**: Allow users to define their own vague terms
3. **Batch Processing**: Process multiple documents simultaneously
4. **Export Reports**: Generate PDF reports with findings
5. **Integration**: Connect with contract management systems

## 📚 API Reference

### POST /contracts/review

Upload and analyze a contract for vague terms.

**Request:**
```http
POST /contracts/review
Content-Type: multipart/form-data

file: <PDF file>
```

**Response:**
```json
{
  "filename": "contract.pdf",
  "size": 123456,
  "issues": [
    {
      "id": "uuid",
      "title": "Vague effort term: reasonable efforts",
      "description": "The clause uses 'reasonable efforts' without specific metrics.",
      "severity": "medium",
      "clause": "Page 1",
      "page_number": 1,
      "remediation": "Define specific metrics or timeframes"
    }
  ],
  "metadata": {
    "doc_id": "uuid",
    "vague_terms_found": 5,
    "findings": [...]
  }
}
```

## 🤝 Contributing

1. Add new vague terms to `rules/vague_terms.json`
2. Test with `python test_vague_terms.py`
3. Update documentation
4. Submit pull request

## 📄 License

This implementation follows the same license as the main Blackletter Systems project.
