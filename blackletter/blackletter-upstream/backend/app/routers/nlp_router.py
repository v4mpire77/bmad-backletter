"""
NLP Router - FastAPI endpoints for NLP functionality
Provides REST API access to text analysis, corpus management, and model operations.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
import json
import logging
from pathlib import Path
import pandas as pd

from ..core.nlp_engine import NLPEngine
from ..services.corpus_gatherer import CorpusGatherer

# Configure logging
logger = logging.getLogger(__name__)

# Initialize components
nlp_engine = NLPEngine()
corpus_gatherer = CorpusGatherer()

# Create router
router = APIRouter(prefix="/nlp", tags=["NLP"])

# Pydantic models for request/response
class TextAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")
    analysis_types: List[str] = Field(
        default=["sentiment", "entities", "keywords", "readability"],
        description="Types of analysis to perform"
    )
    model_name: Optional[str] = Field(None, description="Specific model to use")

class CorpusCollectionRequest(BaseModel):
    sources: List[str] = Field(..., description="Sources to collect from")
    query: Optional[str] = Field(None, description="Search query")
    max_items: int = Field(default=100, description="Maximum items per source")
    date_from: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    date_to: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")

class TopicExtractionRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to analyze")
    num_topics: int = Field(default=5, description="Number of topics to extract")
    method: str = Field(default="lda", description="Topic extraction method")

class ClusteringRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to cluster")
    num_clusters: int = Field(default=5, description="Number of clusters")
    method: str = Field(default="kmeans", description="Clustering method")

class SummaryRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")
    max_length: int = Field(default=150, description="Maximum summary length")
    model_name: Optional[str] = Field(None, description="Summarization model")

@router.post("/analyze")
async def analyze_text(request: TextAnalysisRequest) -> Dict[str, Any]:
    """
    Perform comprehensive text analysis.
    
    Args:
        request: Text analysis request
        
    Returns:
        Analysis results
    """
    try:
        results = {}
        
        if "sentiment" in request.analysis_types:
            results["sentiment"] = nlp_engine.analyze_sentiment(
                request.text, request.model_name
            )
            
        if "entities" in request.analysis_types:
            results["entities"] = nlp_engine.extract_entities(
                request.text, request.model_name
            )
            
        if "keywords" in request.analysis_types:
            results["keywords"] = nlp_engine.extract_keywords(request.text)
            
        if "readability" in request.analysis_types:
            results["readability"] = nlp_engine.analyze_readability(request.text)
            
        if "summary" in request.analysis_types:
            results["summary"] = nlp_engine.generate_summary(
                request.text, model_name=request.model_name
            )
            
        if "comprehensive" in request.analysis_types:
            results = nlp_engine.comprehensive_analysis(request.text)
            
        return {
            "success": True,
            "text_length": len(request.text),
            "analysis": results
        }
        
    except Exception as e:
        logger.error(f"Error in text analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sentiment")
async def analyze_sentiment(request: TextAnalysisRequest) -> Dict[str, Any]:
    """Analyze sentiment of text."""
    try:
        sentiment = nlp_engine.analyze_sentiment(request.text, request.model_name)
        return {
            "success": True,
            "sentiment": sentiment,
            "text": request.text[:100] + "..." if len(request.text) > 100 else request.text
        }
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/entities")
async def extract_entities(request: TextAnalysisRequest) -> Dict[str, Any]:
    """Extract named entities from text."""
    try:
        entities = nlp_engine.extract_entities(request.text, request.model_name)
        return {
            "success": True,
            "entities": entities,
            "count": len(entities)
        }
    except Exception as e:
        logger.error(f"Error in entity extraction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keywords")
async def extract_keywords(request: TextAnalysisRequest) -> Dict[str, Any]:
    """Extract keywords from text."""
    try:
        keywords = nlp_engine.extract_keywords(request.text)
        return {
            "success": True,
            "keywords": keywords,
            "count": len(keywords)
        }
    except Exception as e:
        logger.error(f"Error in keyword extraction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summary")
async def generate_summary(request: SummaryRequest) -> Dict[str, Any]:
    """Generate summary of text."""
    try:
        summary = nlp_engine.generate_summary(
            request.text, request.max_length, request.model_name
        )
        return {
            "success": True,
            "summary": summary,
            "original_length": len(request.text),
            "summary_length": len(summary),
            "compression_ratio": len(summary) / len(request.text) if request.text else 0
        }
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics")
async def extract_topics(request: TopicExtractionRequest) -> Dict[str, Any]:
    """Extract topics from a collection of texts."""
    try:
        topics = nlp_engine.extract_topics(
            request.texts, request.num_topics, request.method
        )
        return {
            "success": True,
            "topics": topics,
            "num_texts": len(request.texts),
            "num_topics": request.num_topics
        }
    except Exception as e:
        logger.error(f"Error in topic extraction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cluster")
async def cluster_texts(request: ClusteringRequest) -> Dict[str, Any]:
    """Cluster texts based on similarity."""
    try:
        clusters = nlp_engine.cluster_texts(
            request.texts, request.num_clusters, request.method
        )
        return {
            "success": True,
            "clusters": clusters,
            "num_texts": len(request.texts),
            "num_clusters": request.num_clusters
        }
    except Exception as e:
        logger.error(f"Error in text clustering: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embeddings")
async def get_embeddings(request: TextAnalysisRequest) -> Dict[str, Any]:
    """Get embeddings for text."""
    try:
        embeddings = nlp_engine.get_embeddings(request.text, request.model_name)
        return {
            "success": True,
            "embeddings": embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings,
            "shape": embeddings.shape if hasattr(embeddings, 'shape') else len(embeddings),
            "text": request.text[:100] + "..." if len(request.text) > 100 else request.text
        }
    except Exception as e:
        logger.error(f"Error in embedding generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preprocess")
async def preprocess_text(request: TextAnalysisRequest) -> Dict[str, Any]:
    """Preprocess text for analysis."""
    try:
        preprocessed = nlp_engine.preprocess_text(request.text)
        return {
            "success": True,
            "original": request.text,
            "preprocessed": preprocessed,
            "original_length": len(request.text),
            "preprocessed_length": len(preprocessed)
        }
    except Exception as e:
        logger.error(f"Error in text preprocessing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Corpus Management Endpoints
@router.post("/corpus/collect")
async def collect_corpus(
    request: CorpusCollectionRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Collect corpus data from multiple sources.
    This is a long-running task that runs in the background.
    """
    try:
        # Start collection in background
        background_tasks.add_task(
            corpus_gatherer.collect_corpus,
            sources=request.sources,
            query=request.query,
            max_items=request.max_items,
            date_from=request.date_from,
            date_to=request.date_to
        )
        
        return {
            "success": True,
            "message": "Corpus collection started in background",
            "sources": request.sources,
            "query": request.query,
            "max_items": request.max_items
        }
    except Exception as e:
        logger.error(f"Error starting corpus collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/corpus/collect-sync")
async def collect_corpus_sync(request: CorpusCollectionRequest) -> Dict[str, Any]:
    """Collect corpus data synchronously (for smaller collections)."""
    try:
        results = corpus_gatherer.collect_corpus(
            sources=request.sources,
            query=request.query,
            max_items=request.max_items,
            date_from=request.date_from,
            date_to=request.date_to
        )
        
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in corpus collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/corpus/process")
async def process_corpus(input_files: Optional[List[str]] = None) -> Dict[str, Any]:
    """Process collected corpus data."""
    try:
        df = corpus_gatherer.process_corpus(input_files)
        stats = corpus_gatherer.get_corpus_stats(df)
        
        return {
            "success": True,
            "stats": stats,
            "dataframe_shape": df.shape,
            "columns": df.columns.tolist()
        }
    except Exception as e:
        logger.error(f"Error processing corpus: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/corpus/stats")
async def get_corpus_stats() -> Dict[str, Any]:
    """Get statistics about the processed corpus."""
    try:
        stats = corpus_gatherer.get_corpus_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting corpus stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/corpus/filter")
async def filter_corpus(
    min_words: int = 10,
    max_words: Optional[int] = None,
    sources: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Filter corpus based on criteria."""
    try:
        # Load processed corpus
        processed_file = corpus_gatherer.output_dir / "processed" / "corpus_processed.csv"
        if not processed_file.exists():
            raise HTTPException(status_code=404, detail="No processed corpus found")
            
        df = pd.read_csv(processed_file)
        filtered_df = corpus_gatherer.filter_corpus(
            df, min_words, max_words, sources, keywords
        )
        
        return {
            "success": True,
            "original_count": len(df),
            "filtered_count": len(filtered_df),
            "filtered_data": filtered_df.head(10).to_dict('records')  # First 10 items
        }
    except Exception as e:
        logger.error(f"Error filtering corpus: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Model Management Endpoints
@router.get("/models/available")
async def get_available_models() -> Dict[str, Any]:
    """Get list of available models."""
    try:
        return {
            "success": True,
            "default_models": nlp_engine.default_models,
            "cached_models": list(nlp_engine.model_cache.keys())
        }
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/load")
async def load_model(model_name: str, task: str) -> Dict[str, Any]:
    """Load a specific model."""
    try:
        model = nlp_engine.load_model(model_name, task)
        if model:
            return {
                "success": True,
                "model_name": model_name,
                "task": task,
                "loaded": True
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to load model")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/save")
async def save_model(model_name: str, task: str) -> Dict[str, Any]:
    """Save a loaded model to disk."""
    try:
        model = nlp_engine.load_model(model_name, task)
        if model:
            nlp_engine.save_model(model, f"{model_name}_{task}")
            return {
                "success": True,
                "model_name": model_name,
                "task": task,
                "saved": True
            }
        else:
            raise HTTPException(status_code=400, detail="Model not found")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# File Upload Endpoints
@router.post("/upload/text")
async def upload_text_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload and analyze a text file."""
    try:
        if not file.filename.endswith(('.txt', '.md', '.csv', '.json')):
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
        content = await file.read()
        text = content.decode('utf-8')
        
        # Perform comprehensive analysis
        analysis = nlp_engine.comprehensive_analysis(text)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(content),
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error processing uploaded file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/corpus")
async def upload_corpus_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload a corpus file (CSV, JSON) for processing."""
    try:
        if not file.filename.endswith(('.csv', '.json')):
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
        content = await file.read()
        
        # Save uploaded file
        upload_dir = corpus_gatherer.output_dir / "uploads"
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, 'wb') as f:
            f.write(content)
            
        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(content),
            "saved_to": str(file_path)
        }
    except Exception as e:
        logger.error(f"Error uploading corpus file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health Check and Info Endpoints
@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "nlp_engine": "initialized",
        "corpus_gatherer": "initialized",
        "device": nlp_engine.device
    }

@router.get("/info")
async def get_nlp_info() -> Dict[str, Any]:
    """Get NLP system information."""
    return {
        "nlp_engine_version": "1.0.0",
        "corpus_gatherer_version": "1.0.0",
        "available_sources": list(corpus_gatherer.collectors.keys()),
        "available_analysis_types": [
            "sentiment", "entities", "keywords", "readability", 
            "summary", "topics", "clustering", "embeddings"
        ],
        "device": nlp_engine.device,
        "models_dir": str(nlp_engine.models_dir),
        "corpus_dir": str(corpus_gatherer.output_dir)
    }
