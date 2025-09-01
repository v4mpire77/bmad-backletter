# NLP System Documentation

## Overview

The NLP (Natural Language Processing) system provides comprehensive text analysis capabilities including sentiment analysis, entity extraction, keyword extraction, summarization, topic modeling, and more. It also includes a powerful corpus gathering system that can collect text data from multiple sources.

## Features

### Text Analysis
- **Sentiment Analysis**: Analyze the emotional tone of text
- **Entity Extraction**: Identify named entities (people, places, organizations)
- **Keyword Extraction**: Extract important keywords and phrases
- **Readability Analysis**: Calculate various readability metrics
- **Text Summarization**: Generate concise summaries
- **Topic Modeling**: Extract topics from collections of texts
- **Text Clustering**: Group similar texts together
- **Embedding Generation**: Create vector representations of text

### Corpus Management
- **Multi-source Data Collection**: News, Wikipedia, academic papers, social media
- **Data Processing**: Clean and structure collected data
- **Corpus Statistics**: Detailed analytics on collected data
- **Filtering**: Filter corpus based on various criteria

### Model Management
- **Model Loading**: Dynamic loading of transformer models
- **Model Caching**: Efficient model reuse
- **Model Persistence**: Save and load custom models

## Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (optional, for faster processing)

### Dependencies
All dependencies are listed in `requirements.txt`. Key packages include:
- `transformers`: Hugging Face transformer models
- `torch`: PyTorch for deep learning
- `spacy`: Advanced NLP processing
- `nltk`: Natural language toolkit
- `sentence-transformers`: Text embeddings
- `scikit-learn`: Machine learning utilities
- `pandas`: Data manipulation
- `fastapi`: Web API framework

### Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download required models:
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

3. Initialize the system:
```bash
python -c "from app.core.nlp_engine import NLPEngine; NLPEngine()"
```

## Usage

### Command Line Interface

The system provides a comprehensive CLI for easy interaction:

```bash
# Analyze text
python scripts/nlp_cli.py analyze text "Your text here"

# Analyze text file
python scripts/nlp_cli.py analyze text --file input.txt --output results.json

# Collect corpus data
python scripts/nlp_cli.py corpus collect --sources news wikipedia --query "artificial intelligence" --max-items 100

# Process collected corpus
python scripts/nlp_cli.py corpus process

# Get corpus statistics
python scripts/nlp_cli.py corpus stats

# Run demo
python scripts/nlp_cli.py demo

# Show system info
python scripts/nlp_cli.py info
```

### Python API

#### Basic Text Analysis
```python
from app.core.nlp_engine import NLPEngine

# Initialize engine
nlp = NLPEngine()

# Analyze text
text = "Natural Language Processing is amazing!"
analysis = nlp.comprehensive_analysis(text)

print(f"Sentiment: {analysis['sentiment']}")
print(f"Keywords: {analysis['keywords']}")
print(f"Entities: {analysis['entities']}")
```

#### Corpus Collection
```python
from app.services.corpus_gatherer import CorpusGatherer

# Initialize gatherer
gatherer = CorpusGatherer()

# Collect data
results = gatherer.collect_corpus(
    sources=['news', 'wikipedia'],
    query='machine learning',
    max_items=100
)

# Process corpus
df = gatherer.process_corpus()

# Get statistics
stats = gatherer.get_corpus_stats(df)
```

## API Endpoints

### Text Analysis

#### POST `/api/nlp/analyze`
Comprehensive text analysis with multiple analysis types.

**Request:**
```json
{
  "text": "Your text to analyze",
  "analysis_types": ["sentiment", "entities", "keywords", "readability"],
  "model_name": "optional_specific_model"
}
```

**Response:**
```json
{
  "success": true,
  "text_length": 123,
  "analysis": {
    "sentiment": {...},
    "entities": [...],
    "keywords": [...],
    "readability": {...}
  }
}
```

#### POST `/api/nlp/sentiment`
Analyze sentiment of text.

#### POST `/api/nlp/entities`
Extract named entities from text.

#### POST `/api/nlp/keywords`
Extract keywords from text.

#### POST `/api/nlp/summary`
Generate summary of text.

#### POST `/api/nlp/topics`
Extract topics from multiple texts.

#### POST `/api/nlp/cluster`
Cluster texts based on similarity.

### Corpus Management

#### POST `/api/nlp/corpus/collect`
Start corpus collection in background.

#### POST `/api/nlp/corpus/collect-sync`
Collect corpus data synchronously.

#### POST `/api/nlp/corpus/process`
Process collected corpus data.

#### GET `/api/nlp/corpus/stats`
Get corpus statistics.

#### POST `/api/nlp/corpus/filter`
Filter corpus based on criteria.

### Model Management

#### GET `/api/nlp/models/available`
List available models.

#### POST `/api/nlp/models/load`
Load a specific model.

#### POST `/api/nlp/models/save`
Save a model to disk.

### File Upload

#### POST `/api/nlp/upload/text`
Upload and analyze a text file.

#### POST `/api/nlp/upload/corpus`
Upload a corpus file for processing.

### System Information

#### GET `/api/nlp/health`
Health check endpoint.

#### GET `/api/nlp/info`
Get system information.

## Configuration

### Environment Variables
- `CUDA_VISIBLE_DEVICES`: Specify GPU devices to use
- `TRANSFORMERS_CACHE`: Set cache directory for transformer models
- `TORCH_HOME`: Set PyTorch model cache directory

### Model Configuration
Default models can be customized in the `NLPEngine` class:

```python
default_models = {
    'sentiment': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
    'emotion': 'j-hartmann/emotion-english-distilroberta-base',
    'ner': 'dslim/bert-base-NER',
    'summarization': 'facebook/bart-large-cnn',
    'question_answering': 'deepset/roberta-base-squad2',
    'zero_shot': 'facebook/bart-large-mnli',
    'embedding': 'sentence-transformers/all-MiniLM-L6-v2'
}
```

## Data Sources

### Available Sources
- **News**: RSS feeds from major news outlets
- **Wikipedia**: Articles and pages
- **Academic**: arXiv papers and Google Scholar
- **YouTube**: Video transcripts
- **Reddit**: Posts and comments
- **Twitter**: Tweets and conversations
- **Web**: General web content scraping

### Source Configuration
Each source can be configured with:
- Query filters
- Date ranges
- Maximum item limits
- Custom parameters

## Performance

### Optimization Tips
1. **Use GPU**: Enable CUDA for faster processing
2. **Model Caching**: Models are automatically cached for reuse
3. **Batch Processing**: Process multiple texts together when possible
4. **Async Processing**: Use background tasks for large corpus collection

### Benchmarks
Typical performance on CPU (Intel i7):
- Sentiment Analysis: ~0.5s per text
- Entity Extraction: ~1s per text
- Keyword Extraction: ~0.3s per text
- Summarization: ~2s per text

With GPU acceleration, these times can be reduced by 5-10x.

## Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/test_nlp_system.py -v

# Run specific test class
python -m pytest tests/test_nlp_system.py::TestNLPEngine -v

# Run with coverage
python -m pytest tests/test_nlp_system.py --cov=app --cov-report=html
```

### Run Benchmarks
```bash
python tests/test_nlp_system.py
```

## Examples

### Example 1: Analyze Customer Feedback
```python
from app.core.nlp_engine import NLPEngine

nlp = NLPEngine()

feedback = """
The product is amazing! I love how easy it is to use.
The customer service was excellent and the delivery was fast.
I would definitely recommend this to others.
"""

analysis = nlp.comprehensive_analysis(feedback)

print(f"Sentiment: {analysis['sentiment']['label']}")
print(f"Top Keywords: {[kw[0] for kw in analysis['keywords'][:5]]}")
print(f"Readability Score: {analysis['readability']['flesch_reading_ease']:.1f}")
```

### Example 2: Build Topic Model from Documents
```python
from app.core.nlp_engine import NLPEngine

nlp = NLPEngine()

documents = [
    "Machine learning algorithms are transforming industries.",
    "Deep learning neural networks achieve remarkable accuracy.",
    "Natural language processing enables human-computer interaction.",
    "Computer vision systems can identify objects in images.",
    "Data science techniques help extract insights from data."
]

topics = nlp.extract_topics(documents, num_topics=3, method="lda")

for topic in topics['topics']:
    print(f"Topic: {topic['words']}")
```

### Example 3: Collect and Analyze News Corpus
```python
from app.services.corpus_gatherer import CorpusGatherer
from app.core.nlp_engine import NLPEngine

# Collect news articles
gatherer = CorpusGatherer()
results = gatherer.collect_corpus(
    sources=['news'],
    query='artificial intelligence',
    max_items=50
)

# Process corpus
df = gatherer.process_corpus()

# Analyze articles
nlp = NLPEngine()
sentiments = []

for text in df['text'].head(10):
    sentiment = nlp.analyze_sentiment(text)
    sentiments.append(sentiment['label'])

print(f"Sentiment distribution: {pd.Series(sentiments).value_counts()}")
```

## Troubleshooting

### Common Issues

1. **Model Download Failures**
   - Check internet connection
   - Verify sufficient disk space
   - Try downloading models manually

2. **Memory Issues**
   - Reduce batch sizes
   - Use smaller models
   - Enable model offloading

3. **Performance Issues**
   - Enable GPU acceleration
   - Use model caching
   - Optimize text preprocessing

4. **API Rate Limits**
   - Implement retry logic
   - Use API keys where available
   - Respect rate limits

### Debug Mode
Enable verbose logging:
```bash
python scripts/nlp_cli.py --verbose analyze text "test"
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a virtual environment
3. Install development dependencies
4. Run tests before making changes
5. Follow PEP 8 style guidelines

### Adding New Features
1. Create feature branch
2. Implement functionality
3. Add tests
4. Update documentation
5. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed information
- Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Comprehensive NLP engine
- Multi-source corpus gathering
- REST API endpoints
- Command-line interface
- Extensive test suite
