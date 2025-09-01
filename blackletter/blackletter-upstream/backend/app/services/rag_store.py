"""
RAG Store Service

Handles text chunking, embedding, and retrieval for contract analysis.
"""
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

@dataclass
class TextChunk:
    """Represents a chunk of contract text with metadata."""
    id: str
    doc_id: str
    text: str
    start_pos: int
    end_pos: int
    page: Optional[int] = None
    section: Optional[str] = None
    embedding: Optional[List[float]] = None

class RAGStore:
    """Vector store for contract text chunks and retrieval."""
    
    def __init__(self, embedding_dim: int = 768):
        """Initialize the RAG store."""
        self.embedding_dim = embedding_dim
        self.chunks: Dict[str, TextChunk] = {}
        self.embeddings: Dict[str, List[float]] = {}
        
    def chunk_text(self, text: str, doc_id: str, chunk_size: int = 1000, overlap: int = 200) -> List[TextChunk]:
        """
        Split text into overlapping chunks for embedding.
        
        Args:
            text: Full contract text
            doc_id: Document identifier
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            List of TextChunk objects
        """
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence ending within last 100 chars
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size - 100:
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunk_id = self._generate_chunk_id(doc_id, chunk_index)
                chunk = TextChunk(
                    id=chunk_id,
                    doc_id=doc_id,
                    text=chunk_text,
                    start_pos=start,
                    end_pos=end,
                    page=self._estimate_page(start, text)
                )
                chunks.append(chunk)
                self.chunks[chunk_id] = chunk
                chunk_index += 1
            
            # Move start position with overlap
            start = max(start + 1, end - overlap)
            
        return chunks

    async def store_document(self, doc_id: str, text: str, metadata: Dict[str, Any]) -> List[TextChunk]:
        """Chunk the provided text and store placeholder embeddings."""
        chunks = self.chunk_text(text, doc_id)
        # Use zero vectors as placeholder embeddings for testing
        zero_embeddings = [[0.0] * self.embedding_dim for _ in chunks]
        self.embed_chunks(chunks, zero_embeddings)
        return chunks

    def embed_chunks(self, chunks: List[TextChunk], embeddings: List[List[float]]) -> None:
        """
        Store embeddings for text chunks.
        
        Args:
            chunks: List of text chunks
            embeddings: Corresponding embeddings from LLM
        """
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
            self.embeddings[chunk.id] = embedding
    
    def retrieve_similar(self, query_embedding: List[float], top_k: int = 5, 
                        doc_id: Optional[str] = None) -> List[Tuple[TextChunk, float]]:
        """
        Retrieve most similar chunks to query embedding.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            doc_id: Optional filter by document ID
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        if not self.embeddings:
            return []
        
        similarities = []
        for chunk_id, embedding in self.embeddings.items():
            chunk = self.chunks[chunk_id]
            
            # Filter by document if specified
            if doc_id and chunk.doc_id != doc_id:
                continue
                
            similarity = self._cosine_similarity(query_embedding, embedding)
            similarities.append((chunk, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def get_stats(self) -> Dict[str, Any]:
        """Return basic statistics about the stored chunks and documents."""
        doc_ids = {chunk.doc_id for chunk in self.chunks.values()}
        return {
            "total_chunks": len(self.chunks),
            "total_documents": len(doc_ids),
            "document_ids": list(doc_ids),
        }
    
    def get_context_around_chunk(self, chunk_id: str, context_chunks: int = 2) -> str:
        """
        Get expanded context around a specific chunk.
        
        Args:
            chunk_id: Target chunk ID
            context_chunks: Number of chunks before/after to include
            
        Returns:
            Expanded context text
        """
        if chunk_id not in self.chunks:
            return ""
        
        target_chunk = self.chunks[chunk_id]
        doc_chunks = [c for c in self.chunks.values() if c.doc_id == target_chunk.doc_id]
        doc_chunks.sort(key=lambda c: c.start_pos)
        
        # Find target chunk index
        target_idx = next((i for i, c in enumerate(doc_chunks) if c.id == chunk_id), -1)
        if target_idx == -1:
            return target_chunk.text
        
        # Get surrounding chunks
        start_idx = max(0, target_idx - context_chunks)
        end_idx = min(len(doc_chunks), target_idx + context_chunks + 1)
        
        context_text = " ".join(c.text for c in doc_chunks[start_idx:end_idx])
        return context_text
    
    def _generate_chunk_id(self, doc_id: str, chunk_index: int) -> str:
        """Generate unique chunk ID."""
        return f"{doc_id}_chunk_{chunk_index:04d}"
    
    def _estimate_page(self, char_pos: int, full_text: str) -> int:
        """Estimate page number based on character position."""
        # Rough estimate: 2500 chars per page
        return (char_pos // 2500) + 1
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
            
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def clear_document(self, doc_id: str) -> None:
        """Remove all chunks and embeddings for a document."""
        chunk_ids_to_remove = [cid for cid, chunk in self.chunks.items() if chunk.doc_id == doc_id]
        for chunk_id in chunk_ids_to_remove:
            del self.chunks[chunk_id]
            if chunk_id in self.embeddings:
                del self.embeddings[chunk_id]


# Global instance used across the application
rag_store = RAGStore()
