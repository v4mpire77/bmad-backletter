"""
Research query service for Blackletter Systems.

This module provides functionality for legal research:
- Query the vector database
- Generate answers with citations
- Ingest documents into the corpus
"""

import os
import time
import io
from typing import Dict, List, Optional, Any
import logging
import json

from fastapi import UploadFile

from app.core.llm_adapter import generate
from app.core.vectors import search_documents, add_document, batch_add_documents
from app.core.storage import upload_file, download_file
from app.core.ocr import extract_text
from app.core.citations import extract_citations, Citation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def query_research(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Query the research system.
    
    Args:
        query: Research query
        filters: Optional filters
        limit: Maximum number of results
        
    Returns:
        Dict[str, Any]: Query results
    """
    try:
        # Search the vector database
        logger.info(f"Searching for: {query}")
        search_results = await search_documents(
            query=query,
            limit=limit,
            source_type=filters.get("source_type") if filters else None,
            source=filters.get("source") if filters else None
        )
        
        # Format results for the LLM
        context = "I need to answer a legal research question based on the following sources:\n\n"
        
        for i, result in enumerate(search_results, 1):
            context += f"Source {i}:\n"
            context += f"Content: {result['content']}\n"
            
            if "source" in result:
                context += f"Source: {result['source']}\n"
            
            if "page" in result:
                context += f"Page: {result['page']}\n"
            
            if "paragraph" in result:
                context += f"Paragraph: {result['paragraph']}\n"
            
            context += "\n"
        
        # Generate answer with LLM
        prompt = f"{context}\nQuestion: {query}\n\nPlease provide a comprehensive answer based on the sources above. Include specific citations to the sources in your answer using the format [Source X, Paragraph Y]. Ensure your answer is accurate, well-reasoned, and directly addresses the question."
        
        system_prompt = "You are a legal research assistant specialized in UK and EU law. Provide accurate, well-reasoned answers based on the provided sources. Always include specific citations to your sources."
        
        answer = await generate(prompt, system_prompt)
        
        # Extract citations from the answer
        citations = []
        
        # Look for [Source X, Paragraph Y] pattern
        import re
        citation_matches = re.finditer(r'\[Source (\d+)(?:, Paragraph (\d+))?\]', answer)
        
        for match in citation_matches:
            source_num = int(match.group(1))
            para_num = int(match.group(2)) if match.group(2) else None
            
            if 1 <= source_num <= len(search_results):
                source = search_results[source_num - 1]
                
                citation = {
                    "text": match.group(0),
                    "case_id": source.get("source", f"Source {source_num}"),
                    "para": para_num or source.get("paragraph"),
                    "source_type": source.get("sourceType", "case"),
                    "source_id": source.get("id")
                }
                
                citations.append(citation)
        
        # Format search results
        formatted_results = []
        
        for result in search_results:
            formatted_result = {
                "text": result["content"],
                "source": result.get("source", "Unknown"),
                "score": result.get("score", 0.0),
                "page": result.get("page"),
                "paragraph": result.get("paragraph")
            }
            
            if "metadata" in result:
                formatted_result["metadata"] = result["metadata"]
            
            formatted_results.append(formatted_result)
        
        return {
            "answer": answer,
            "citations": citations,
            "results": formatted_results
        }
    
    except Exception as e:
        logger.error(f"Error querying research system: {str(e)}")
        raise

async def ingest_document(
    file: UploadFile,
    source_type: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Ingest a document into the research corpus.
    
    Args:
        file: Document file
        source_type: Type of source
        metadata: Additional metadata
        
    Returns:
        Dict[str, Any]: Ingestion results
    """
    try:
        # Read the file
        file_content = await file.read()
        
        # Upload to storage
        document_key = await upload_file(
            file_data=file_content,
            filename=file.filename,
            folder="corpus",
            content_type=file.content_type,
            metadata=metadata
        )
        
        # Extract text
        text = extract_text(io.BytesIO(file_content))
        
        # Generate a document ID based on content hash
        import hashlib
        document_id = hashlib.md5(text.encode()).hexdigest()
        
        # Split into chunks
        chunks = split_text_into_chunks(text)
        
        # Prepare documents for vector database
        documents = []
        
        for i, chunk in enumerate(chunks):
            doc = {
                "text": chunk["text"],
                "source": file.filename,
                "source_type": source_type,
                "page": chunk.get("page"),
                "paragraph": i + 1,
                "metadata": metadata
            }
            
            documents.append(doc)
        
        # Add to vector database
        doc_ids = await batch_add_documents(documents)
        
        return {
            "document_id": document_id,
            "document_key": document_key,
            "chunks_count": len(chunks)
        }
    
    except Exception as e:
        logger.error(f"Error ingesting document: {str(e)}")
        raise

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to split
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between chunks in characters
        
    Returns:
        List[Dict[str, Any]]: List of text chunks with metadata
    """
    chunks = []
    
    # Split by paragraphs first
    paragraphs = text.split("\n\n")
    
    current_chunk = ""
    current_page = 1
    
    for para in paragraphs:
        # Check for page markers
        if para.strip().startswith("Page ") and len(para.strip()) < 20:
            try:
                current_page = int(para.strip().split(" ")[1])
                continue
            except (IndexError, ValueError):
                pass
        
        # If adding this paragraph would exceed chunk size, save current chunk
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append({
                "text": current_chunk,
                "page": current_page
            })
            
            # Start new chunk with overlap
            words = current_chunk.split()
            if len(words) > overlap // 10:  # Approximate words for overlap
                current_chunk = " ".join(words[-(overlap // 10):]) + "\n\n"
            else:
                current_chunk = ""
        
        # Add paragraph to current chunk
        if current_chunk and not current_chunk.endswith("\n\n"):
            current_chunk += "\n\n"
        
        current_chunk += para
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append({
            "text": current_chunk,
            "page": current_page
        })
    
    return chunks
