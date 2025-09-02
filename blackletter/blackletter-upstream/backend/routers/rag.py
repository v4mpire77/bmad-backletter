"""
RAG Router

Handles RAG-specific endpoints for document storage, retrieval, and semantic search.
"""
from fastapi import APIRouter, HTTPException, UploadFile, Form, Depends, Request
import logging
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

from ..app.core.llm_adapter import LLMAdapter
from ..app.core.ocr import OCRProcessor
from ..app.services.rag_store import rag_store
from ..app.core.auth import verify_supabase_jwt
from ..app.core.security import rate_limit, SecurityMiddleware
from ..models.schemas import UploadResponse, AnalysisProgress

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
llm_adapter = LLMAdapter()
ocr_processor = OCRProcessor()

# In-memory storage for upload tracking (use database in production)
upload_storage = {}

@router.post("/upload", response_model=UploadResponse)
@rate_limit()
async def upload_document(
    file: UploadFile, 
    user=Depends(verify_supabase_jwt),
    request: Request = None
):
    """
    Upload and process a document for RAG storage.
    
    This endpoint:
    1. Extracts text from the uploaded document
    2. Chunks the text into manageable pieces
    3. Stores the chunks in the vector database
    4. Returns document metadata
    """
    try:
        logger.info("RAG upload requested by user_id=%s filename=%s size=%s", user.get("sub"), file.filename, getattr(file, 'size', 'n/a'))
        # Enhanced file validation using security middleware
        content = await file.read()
        is_valid, error_msg = SecurityMiddleware.validate_file_upload(
            content, file.filename or "", file.content_type or ""
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Extract text using OCR or direct reading
        if file.filename.lower().endswith('.pdf'):
            extracted_text = await ocr_processor.extract_text(content)
        else:
            # For text files, decode directly
            extracted_text = content.decode('utf-8', errors='ignore')
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in document")
        
        # Store document metadata
        metadata = {
            "filename": file.filename,
            "size": len(content),
            "upload_time": datetime.utcnow().isoformat(),
            "content_type": file.content_type,
            "text_length": len(extracted_text)
        }
        
        # Store in RAG store
        chunks = await rag_store.store_document(doc_id, extracted_text, metadata)
        
        # Track upload
        upload_storage[doc_id] = {
            "status": "completed",
            "chunks_created": len(chunks),
            "metadata": metadata
        }
        
        logger.info("RAG upload completed: user_id=%s doc_id=%s chunks=%s", user.get("sub"), doc_id, len(chunks))
        return UploadResponse(
            doc_id=doc_id,
            filename=file.filename,
            size=len(content),
            upload_time=metadata["upload_time"]
        )
        
    except Exception as e:
        logger.error("RAG upload failed: user_id=%s filename=%s error=%s", user.get("sub") if isinstance(user, dict) else None, getattr(file, 'filename', None), str(e))
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/query")
@rate_limit()
async def query_documents(
    query: str = Form(...),
    doc_id: Optional[str] = Form(None),
    top_k: int = Form(5),
    use_semantic_search: bool = Form(True),
    user=Depends(verify_supabase_jwt),
    request: Request = None
):
    """
    Query documents using RAG.
    
    This endpoint:
    1. Takes a natural language query
    2. Retrieves relevant document chunks
    3. Generates a response using the retrieved context
    """
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Get query embedding
        query_embedding = await llm_adapter.get_embeddings([query])
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate query embedding")
        
        # Retrieve similar chunks
        if use_semantic_search:
            similar_chunks = await rag_store.semantic_search(query, top_k, doc_id)
        else:
            similar_chunks = await rag_store.retrieve_similar(query_embedding[0], top_k, doc_id)
        
        if not similar_chunks:
            return {
                "answer": "No relevant information found in the documents.",
                "chunks": [],
                "query": query
            }
        
        # Extract chunk texts for context
        context_chunks = [chunk.text for chunk, score in similar_chunks]
        
        # Generate response using context
        answer = await llm_adapter.generate_with_context(query, context_chunks)
        
        # Prepare response with citations
        chunk_details = []
        for chunk, score in similar_chunks:
            chunk_details.append({
                "id": chunk.id,
                "text": chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                "page": chunk.page,
                "similarity_score": round(score, 3),
                "start_pos": chunk.start_pos,
                "end_pos": chunk.end_pos
            })
        
        return {
            "answer": answer,
            "chunks": chunk_details,
            "query": query,
            "total_chunks_retrieved": len(similar_chunks)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/documents/{doc_id}/chunks")
async def get_document_chunks(doc_id: str):
    """
    Get all chunks for a specific document.
    """
    try:
        chunks = rag_store.get_document_chunks(doc_id)
        
        chunk_data = []
        for chunk in chunks:
            chunk_data.append({
                "id": chunk.id,
                "text": chunk.text,
                "page": chunk.page,
                "start_pos": chunk.start_pos,
                "end_pos": chunk.end_pos,
                "metadata": chunk.metadata
            })
        
        return {
            "doc_id": doc_id,
            "total_chunks": len(chunks),
            "chunks": chunk_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving document chunks: {str(e)}")

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, user=Depends(verify_supabase_jwt)):
    """
    Delete a document and all its chunks from the RAG store.
    """
    try:
        rag_store.clear_document(doc_id)
        
        # Remove from upload tracking
        if doc_id in upload_storage:
            del upload_storage[doc_id]
        
        return {"message": f"Document {doc_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@router.get("/documents")
async def list_documents(user=Depends(verify_supabase_jwt)):
    """
    List all documents in the RAG store.
    """
    try:
        # Get stats from RAG store
        stats = rag_store.get_stats()
        
        # Get document list from upload storage
        documents = []
        for doc_id, data in upload_storage.items():
            documents.append({
                "doc_id": doc_id,
                "filename": data["metadata"]["filename"],
                "upload_time": data["metadata"]["upload_time"],
                "size": data["metadata"]["size"],
                "chunks_created": data["chunks_created"],
                "status": data["status"]
            })
        
        return {
            "documents": documents,
            "total_documents": len(documents),
            "rag_stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.get("/stats")
async def get_rag_stats(user=Depends(verify_supabase_jwt)):
    """
    Get statistics about the RAG store.
    """
    try:
        stats = rag_store.get_stats()
        return {
            "rag_store": stats,
            "upload_tracking": {
                "total_uploads": len(upload_storage),
                "completed_uploads": len([u for u in upload_storage.values() if u["status"] == "completed"])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@router.post("/search")
async def search_documents(
    query: str = Form(...),
    doc_id: Optional[str] = Form(None),
    top_k: int = Form(10),
    similarity_threshold: float = Form(0.7),
    user=Depends(verify_supabase_jwt)
):
    """
    Search for specific content in documents.
    
    This endpoint performs semantic search and returns matching chunks
    without generating a response.
    """
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Perform semantic search
        results = await rag_store.semantic_search(query, top_k, doc_id)
        
        # Filter by similarity threshold
        filtered_results = [(chunk, score) for chunk, score in results if score >= similarity_threshold]
        
        # Prepare response
        search_results = []
        for chunk, score in filtered_results:
            search_results.append({
                "id": chunk.id,
                "doc_id": chunk.doc_id,
                "text": chunk.text,
                "page": chunk.page,
                "similarity_score": round(score, 3),
                "start_pos": chunk.start_pos,
                "end_pos": chunk.end_pos,
                "metadata": chunk.metadata
            })
        
        return {
            "query": query,
            "results": search_results,
            "total_results": len(search_results),
            "similarity_threshold": similarity_threshold
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")

@router.post("/batch-query")
async def batch_query_documents(
    queries: List[str] = Form(...),
    doc_id: Optional[str] = Form(None),
    top_k: int = Form(5),
    user=Depends(verify_supabase_jwt)
):
    """
    Process multiple queries in batch.
    """
    try:
        if not queries:
            raise HTTPException(status_code=400, detail="No queries provided")
        
        if len(queries) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 queries allowed per batch")
        
        results = []
        for query in queries:
            try:
                # Get query embedding
                query_embedding = await llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                # Retrieve similar chunks
                similar_chunks = await rag_store.retrieve_similar(query_embedding[0], top_k, doc_id)
                
                # Generate response
                context_chunks = [chunk.text for chunk, score in similar_chunks]
                answer = await llm_adapter.generate_with_context(query, context_chunks)
                
                results.append({
                    "query": query,
                    "answer": answer,
                    "chunks_retrieved": len(similar_chunks)
                })
                
            except Exception as e:
                results.append({
                    "query": query,
                    "error": str(e),
                    "answer": None,
                    "chunks_retrieved": 0
                })
        
        return {
            "batch_results": results,
            "total_queries": len(queries),
            "successful_queries": len([r for r in results if r.get("answer")])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch queries: {str(e)}")
