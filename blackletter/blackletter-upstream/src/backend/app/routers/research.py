"""
Research router for Blackletter Systems.

This module provides API endpoints for legal research:
- Query the RAG system
- Ingest documents
- Manage the corpus
"""

import time
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, Query

from app.models.schemas import (
    ResearchQueryRequest, ResearchQueryResponse,
    ResearchResult, Citation
)
from app.services.research_query import query_research, ingest_document

router = APIRouter()

@router.post("/query", response_model=ResearchQueryResponse)
async def query(request: ResearchQueryRequest):
    """
    Query the research system.
    
    Args:
        request: Research query request
        
    Returns:
        ResearchQueryResponse: Query response with results
    """
    try:
        # Start timing
        start_time = time.time()
        
        # Query the research system
        query_result = await query_research(
            query=request.query,
            filters=request.filters,
            limit=request.limit
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create response
        response = ResearchQueryResponse(
            query=request.query,
            answer=query_result["answer"],
            citations=query_result["citations"],
            results=query_result["results"],
            processing_time=processing_time
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying research system: {str(e)}")

@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    source_type: str = Form(...),
    metadata: Optional[str] = Form(None)
):
    """
    Ingest a document into the research corpus.
    
    Args:
        file: The document file
        source_type: Type of source document
        metadata: Optional JSON metadata
        
    Returns:
        Dict: Ingestion result
    """
    try:
        # Parse metadata if provided
        parsed_metadata = None
        if metadata:
            import json
            try:
                parsed_metadata = json.loads(metadata)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid metadata JSON")
        
        # Ingest the document
        ingest_result = await ingest_document(
            file=file,
            source_type=source_type,
            metadata=parsed_metadata
        )
        
        return {
            "message": "Document ingested successfully",
            "document_id": ingest_result["document_id"],
            "chunks_count": ingest_result["chunks_count"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting document: {str(e)}")

@router.get("/sources")
async def get_sources(
    source_type: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get available research sources.
    
    Args:
        source_type: Optional filter by source type
        limit: Maximum number of sources to return
        offset: Offset for pagination
        
    Returns:
        List[Dict]: List of available sources
    """
    # This would typically come from a database
    # For now, return some sample sources
    sources = [
        {
            "id": "bailii_uksc",
            "name": "UK Supreme Court Judgments",
            "source_type": "case",
            "url": "https://www.bailii.org/uk/cases/UKSC/"
        },
        {
            "id": "bailii_ewca",
            "name": "England and Wales Court of Appeal Judgments",
            "source_type": "case",
            "url": "https://www.bailii.org/ew/cases/EWCA/"
        },
        {
            "id": "legislation_gov_uk",
            "name": "UK Legislation",
            "source_type": "legislation",
            "url": "https://www.legislation.gov.uk/"
        }
    ]
    
    # Apply source_type filter if provided
    if source_type:
        sources = [s for s in sources if s["source_type"] == source_type]
    
    # Apply pagination
    paginated_sources = sources[offset:offset + limit]
    
    return paginated_sources

@router.get("/statistics")
async def get_statistics():
    """
    Get statistics about the research corpus.
    
    Returns:
        Dict: Corpus statistics
    """
    # This would typically come from the vector database
    # For now, return some sample statistics
    return {
        "documents_count": 1250,
        "chunks_count": 45678,
        "sources": {
            "case": 850,
            "legislation": 350,
            "article": 50
        },
        "last_updated": "2023-08-15T10:30:00Z"
    }
