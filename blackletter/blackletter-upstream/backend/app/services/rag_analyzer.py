"""
RAG Analyzer Service

Integrates RAG capabilities with contract analysis for enhanced legal document processing.
Following Context Engineering Framework standards for consistency, quality, and maintainability.
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid
import logging
from dataclasses import dataclass, field
from collections import defaultdict

from ..core.llm_adapter import LLMAdapter
from .rag_store import rag_store
from .vague_detector import VagueTermsDetector

# Input validation decorator
def validate_input(**validators):
    """
    Decorator for validating method inputs following framework standards.
    
    Args:
        validators: Dictionary of parameter names and their validation functions
        
    Example:
        @validate_input(
            doc_id=lambda x: bool(x and x.strip()),
            text=lambda x: bool(x and len(x.strip()) > 0)
        )
        def my_method(self, doc_id: str, text: str):
            ...
    """
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()
            
            # Get operation name for metrics
            operation_name = func.__name__
            
            # Validate each parameter
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        error_msg = f"Invalid {param_name}: validation failed"
                        if hasattr(self, 'metrics'):
                            self.metrics.record_operation(
                                operation_name=operation_name,
                                success=False,
                                duration_ms=0,
                                error_type="VALIDATION_ERROR"
                            )
                        raise RAGAnalysisError(error_msg)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Enhanced metrics tracking
@dataclass
class RAGMetrics:
    """
    Tracks comprehensive metrics for RAG operations.
    
    Features:
        - Operation tracking (success/failure)
        - Performance monitoring
        - Error analysis
        - Resource usage tracking
        - Batch processing metrics
        
    Performance Targets:
        - Average latency: < 2000ms
        - Error rate: < 1%
        - Success rate: > 95%
        - Resource efficiency: < 100MB per operation
    """
    # Basic operation metrics
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    total_processing_time_ms: float = 0.0
    
    # Detailed error tracking
    error_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    error_details: List[Dict[str, Any]] = field(default_factory=list)
    
    # Performance metrics
    avg_chunk_count: float = 0.0
    operation_latencies: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    peak_memory_usage: Dict[str, float] = field(default_factory=dict)
    
    # Batch processing metrics
    batch_operations: int = 0
    batch_success_rate: float = 0.0
    avg_batch_size: float = 0.0
    batch_processing_times: List[float] = field(default_factory=list)
    
    # Resource usage
    embedding_cache_hits: int = 0
    embedding_cache_misses: int = 0
    total_tokens_processed: int = 0
    avg_memory_per_operation: float = 0.0
    
    def record_operation(
        self,
        operation_name: str,
        success: bool,
        duration_ms: float,
        error_type: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None,
        memory_usage: Optional[float] = None,
        tokens_processed: Optional[int] = None,
        is_batch: bool = False,
        batch_size: Optional[int] = None,
        cache_hit: Optional[bool] = None
    ):
        """
        Record comprehensive metrics for an operation.
        
        Args:
            operation_name: Name of the operation
            success: Whether operation succeeded
            duration_ms: Operation duration in milliseconds
            error_type: Type of error if operation failed
            error_details: Detailed error information
            memory_usage: Peak memory usage in MB
            tokens_processed: Number of tokens processed
            is_batch: Whether this was a batch operation
            batch_size: Size of batch if applicable
            cache_hit: Whether operation hit embedding cache
        """
        # Basic operation tracking
        self.total_operations += 1
        if success:
            self.successful_operations += 1
        else:
            self.failed_operations += 1
            if error_type:
                self.error_counts[error_type] += 1
            if error_details:
                self.error_details.append({
                    "type": error_type,
                    "details": error_details,
                    "timestamp": datetime.utcnow().isoformat(),
                    "operation": operation_name
                })
        
        # Performance metrics
        self.total_processing_time_ms += duration_ms
        self.operation_latencies[operation_name].append(duration_ms)
        
        if memory_usage:
            self.peak_memory_usage[operation_name] = max(
                self.peak_memory_usage.get(operation_name, 0),
                memory_usage
            )
            self.avg_memory_per_operation = (
                (self.avg_memory_per_operation * (self.total_operations - 1) + memory_usage)
                / self.total_operations
            )
        
        # Resource tracking
        if tokens_processed:
            self.total_tokens_processed += tokens_processed
        
        if cache_hit is not None:
            if cache_hit:
                self.embedding_cache_hits += 1
            else:
                self.embedding_cache_misses += 1
        
        # Batch metrics
        if is_batch and batch_size:
            self.batch_operations += 1
            self.batch_processing_times.append(duration_ms)
            self.avg_batch_size = (
                (self.avg_batch_size * (self.batch_operations - 1) + batch_size)
                / self.batch_operations
            )
            if success:
                self.batch_success_rate = (
                    (self.batch_success_rate * (self.batch_operations - 1) + 100)
                    / self.batch_operations
                )
    
    def get_success_rate(self) -> float:
        """Calculate the success rate of operations."""
        return (self.successful_operations / self.total_operations * 100) if self.total_operations > 0 else 0.0
    
    def get_avg_latency(self, operation_name: Optional[str] = None) -> float:
        """Get average latency for all or specific operations."""
        if operation_name:
            latencies = self.operation_latencies.get(operation_name, [])
            return sum(latencies) / len(latencies) if latencies else 0.0
        return self.total_processing_time_ms / self.total_operations if self.total_operations > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary format."""
        return {
            "total_operations": self.total_operations,
            "success_rate": self.get_success_rate(),
            "avg_latency_ms": self.get_avg_latency(),
            "error_distribution": dict(self.error_counts),
            "operation_latencies": {
                op: sum(lats) / len(lats) if lats else 0.0
                for op, lats in self.operation_latencies.items()
            }
        }

# Configure logging following framework standards
logger = logging.getLogger(__name__)

def structured_log(
    logger_instance: logging.Logger,
    level: str,
    message: str,
    correlation_id: str,
    operation: str,
    **kwargs
) -> None:
    """
    Helper function for structured logging following framework standards.
    
    Args:
        logger_instance: Logger instance to use
        level: Log level (info, error, debug, warning)
        message: Log message
        correlation_id: Request correlation ID
        operation: Operation name
        **kwargs: Additional log context
    """
    log_data = {
        "correlation_id": correlation_id,
        "operation": operation,
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }
    
    log_func = getattr(logger_instance, level)
    log_func(message, extra=log_data)

class RAGAnalysisError(Exception):
    """Custom exception for RAG analysis errors."""
    pass

class RAGAnalysisResult:
    """
    Structured result class for RAG analysis operations.
    Ensures consistent response format across the application.
    """
    def __init__(
        self,
        doc_id: str,
        success: bool = True,
        basic_analysis: Optional[Dict[str, Any]] = None,
        rag_insights: Optional[Dict[str, Any]] = None,
        compliance_analysis: Optional[Dict[str, Any]] = None,
        risk_assessment: Optional[Dict[str, Any]] = None,
        vague_terms_found: int = 0,
        chunks_created: int = 0,
        error_message: Optional[str] = None,
        processing_time_ms: Optional[float] = None
    ):
        self.doc_id = doc_id
        self.success = success
        self.basic_analysis = basic_analysis or {}
        self.rag_insights = rag_insights or {}
        self.compliance_analysis = compliance_analysis or {}
        self.risk_assessment = risk_assessment or {}
        self.vague_terms_found = vague_terms_found
        self.chunks_created = chunks_created
        self.error_message = error_message
        self.processing_time_ms = processing_time_ms
        self.analysis_timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format."""
        result = {
            "doc_id": self.doc_id,
            "success": self.success,
            "analysis_timestamp": self.analysis_timestamp,
            "vague_terms_found": self.vague_terms_found,
            "chunks_created": self.chunks_created
        }
        
        if self.success:
            result.update({
                "basic_analysis": self.basic_analysis,
                "rag_insights": self.rag_insights,
                "compliance_analysis": self.compliance_analysis,
                "risk_assessment": self.risk_assessment
            })
        else:
            result["error"] = self.error_message
            
        if self.processing_time_ms:
            result["processing_time_ms"] = self.processing_time_ms
            
        return result

class RAGAnalyzer:
    """
    Enhanced contract analyzer using RAG capabilities.
    
    Integrates RAG capabilities with contract analysis for enhanced legal document processing.
    Following Context Engineering Framework standards for consistency, quality, and maintainability.
    
    Features:
        - Single document analysis
        - Batch document processing
        - Advanced search filters
        - Export capabilities
        - Analytics tracking
    
    Attributes:
        llm_adapter: LLM adapter for AI processing
        vague_detector: Vague terms detection service
        
    Performance Targets:
        - Single analysis completion: < 30 seconds for typical documents
        - Batch processing: < 20 seconds per document
        - Query response time: < 2 seconds
        - Error rate: < 1% for valid inputs
        - Batch success rate: > 95%
    """
    
    def __init__(self) -> None:
        """Initialize RAG analyzer with required services."""
        try:
            self.llm_adapter = LLMAdapter()
            self.vague_detector = VagueTermsDetector()
            self.metrics = RAGMetrics()
            correlation_id = str(uuid.uuid4())
            structured_log(
                logger,
                "info",
                "RAGAnalyzer initialized successfully",
                correlation_id,
                "initialize",
                component="RAGAnalyzer"
            )
        except Exception as e:
            correlation_id = str(uuid.uuid4())
            error_msg = f"Failed to initialize RAGAnalyzer: {str(e)}"
            structured_log(
                logger,
                "error",
                error_msg,
                correlation_id,
                "initialize",
                component="RAGAnalyzer",
                error_type=e.__class__.__name__,
                error_details=str(e)
            )
            raise RAGAnalysisError(error_msg) from e
    
    @validate_input(
        doc_id=lambda x: bool(x and x.strip()),
        text=lambda x: bool(x and x.strip())
    )
    async def analyze_contract_with_rag(
        self, 
        doc_id: str, 
        text: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> RAGAnalysisResult:
        """
        Perform comprehensive contract analysis using RAG.
        
        This method provides enhanced contract analysis by combining traditional NLP
        techniques with RAG capabilities for deeper insights and context awareness.
        
        Args:
            doc_id: Unique document identifier
            text: Contract text content
            metadata: Optional document metadata
            
        Returns:
            RAGAnalysisResult: Structured analysis results
            
        Raises:
            RAGAnalysisError: When analysis fails due to critical errors
            
        Performance:
            Target: < 30 seconds for documents up to 50 pages
            Timeout: 120 seconds maximum
        """
        operation_name = "analyze_contract"
        start_time = datetime.utcnow()
        correlation_id = str(uuid.uuid4())
        
        # Input validation
        if not doc_id or not doc_id.strip():
            error_msg = "Document ID is required"
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=0,
                error_type="VALIDATION_ERROR"
            )
            raise RAGAnalysisError(error_msg)
        
        if not text or not text.strip():
            error_msg = "Document text is required"
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=0,
                error_type="VALIDATION_ERROR"
            )
            raise RAGAnalysisError(error_msg)
        
        structured_log(
            logger,
            "info",
            f"Starting RAG analysis for document {doc_id}",
            correlation_id,
            operation_name,
            doc_id=doc_id
        )
        
        try:
            # Initialize metadata with correlation ID
            metadata = metadata or {}
            metadata["correlation_id"] = correlation_id
            
            # Store document in RAG store
            structured_log(
                logger,
                "debug",
                f"Storing document {doc_id} in RAG store",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                step="store_document"
            )
            chunks = await rag_store.store_document(doc_id, text, metadata)
            structured_log(
                logger,
                "info",
                f"Created {len(chunks)} chunks for document {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                chunks_created=len(chunks)
            )
            
            # Perform basic contract analysis
            structured_log(
                logger,
                "debug",
                f"Performing basic contract analysis for {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                step="basic_analysis"
            )
            basic_analysis = await self.llm_adapter.analyze_contract(text)
            
            # Find vague terms
            structured_log(
                logger,
                "debug",
                f"Detecting vague terms in document {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                step="vague_terms_detection"
            )
            vague_hits = self.vague_detector.find_vague_spans(text)
            structured_log(
                logger,
                "info",
                f"Found {len(vague_hits)} vague terms in document {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                vague_terms_found=len(vague_hits)
            )
            
            # Enhanced analysis using RAG
            structured_log(
                logger,
                "debug",
                f"Generating RAG insights for document {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                step="rag_insights"
            )
            rag_insights = await self._generate_rag_insights(doc_id, text, vague_hits)
            
            # Generate compliance analysis
            structured_log(
                logger,
                "debug",
                f"Performing compliance analysis for document {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                step="compliance_analysis"
            )
            compliance_analysis = await self._analyze_compliance(doc_id, text)
            
            # Generate risk assessment
            structured_log(
                logger,
                "debug",
                f"Performing risk assessment for document {doc_id}",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                step="risk_assessment"
            )
            risk_assessment = await self._assess_risks(doc_id, text)
            
            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Record successful operation metrics
            self.metrics.record_operation(
                operation_name=operation_name,
                success=True,
                duration_ms=processing_time_ms
            )
            
            structured_log(
                logger,
                "info",
                f"RAG analysis completed for document {doc_id} in {processing_time_ms:.2f}ms",
                correlation_id,
                operation_name,
                doc_id=doc_id,
                duration_ms=processing_time_ms,
                chunks_created=len(chunks),
                vague_terms_found=len(vague_hits),
                status="completed"
            )
            
            return RAGAnalysisResult(
                doc_id=doc_id,
                success=True,
                basic_analysis=basic_analysis,
                rag_insights=rag_insights,
                compliance_analysis=compliance_analysis,
                risk_assessment=risk_assessment,
                vague_terms_found=len(vague_hits),
                chunks_created=len(chunks),
                processing_time_ms=processing_time_ms
            )
            
        except RAGAnalysisError:
            # Record error metrics and re-raise
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=0,
                error_type="RAG_ANALYSIS_ERROR"
            )
            raise
            
        except Exception as e:
            # Calculate processing time even for errors
            end_time = datetime.utcnow()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            error_msg = f"Analysis failed for document {doc_id}: {str(e)}"
            structured_log(
                logger,
                "error",
                error_msg,
                correlation_id,
                operation_name,
                doc_id=doc_id,
                error_type=e.__class__.__name__,
                duration_ms=processing_time_ms,
                status="failed",
                exc_info=True
            )
            
            # Record error metrics
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=processing_time_ms,
                error_type=e.__class__.__name__
            )
            
            return RAGAnalysisResult(
                doc_id=doc_id,
                success=False,
                error_message=str(e),
                processing_time_ms=processing_time_ms
            )
    
    async def _generate_rag_insights(self, doc_id: str, text: str, 
                                   vague_hits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights using RAG capabilities."""
        insights = {
            "key_clauses": [],
            "important_dates": [],
            "parties_involved": [],
            "financial_terms": [],
            "termination_conditions": []
        }
        
        # Query for key contract elements
        queries = [
            "What are the key clauses and obligations in this contract?",
            "What are the important dates and deadlines mentioned?",
            "Who are the parties involved in this contract?",
            "What are the financial terms and payment conditions?",
            "What are the termination conditions and exit clauses?"
        ]
        
        for query in queries:
            try:
                # Get query embedding
                query_embedding = await self.llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                # Retrieve relevant chunks
                similar_chunks = await rag_store.retrieve_similar(
                    query_embedding[0], top_k=3, doc_id=doc_id
                )
                
                if similar_chunks:
                    # Generate insight using context
                    context_chunks = [chunk.text for chunk, score in similar_chunks]
                    insight = await self.llm_adapter.generate_with_context(query, context_chunks)
                    
                    # Categorize insight
                    if "date" in query.lower() or "deadline" in query.lower():
                        insights["important_dates"].append(insight)
                    elif "party" in query.lower() or "involved" in query.lower():
                        insights["parties_involved"].append(insight)
                    elif "financial" in query.lower() or "payment" in query.lower():
                        insights["financial_terms"].append(insight)
                    elif "termination" in query.lower() or "exit" in query.lower():
                        insights["termination_conditions"].append(insight)
                    else:
                        insights["key_clauses"].append(insight)
                        
            except Exception as e:
                print(f"Error generating insight for query '{query}': {e}")
        
        return insights
    
    async def _analyze_compliance(self, doc_id: str, text: str) -> Dict[str, Any]:
        """Analyze contract for compliance issues."""
        compliance_queries = [
            "What GDPR compliance issues might exist in this contract?",
            "Are there any data protection or privacy concerns?",
            "What regulatory compliance requirements are mentioned?",
            "Are there any potential legal or regulatory risks?"
        ]
        
        compliance_issues = []
        
        for query in compliance_queries:
            try:
                query_embedding = await self.llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                similar_chunks = await rag_store.retrieve_similar(
                    query_embedding[0], top_k=5, doc_id=doc_id
                )
                
                if similar_chunks:
                    context_chunks = [chunk.text for chunk, score in similar_chunks]
                    analysis = await self.llm_adapter.generate_with_context(query, context_chunks)
                    
                    compliance_issues.append({
                        "query": query,
                        "analysis": analysis,
                        "relevant_chunks": len(similar_chunks)
                    })
                    
            except Exception as e:
                print(f"Error analyzing compliance for query '{query}': {e}")
        
        return {
            "compliance_issues": compliance_issues,
            "total_issues_identified": len(compliance_issues)
        }
    
    async def _assess_risks(self, doc_id: str, text: str) -> Dict[str, Any]:
        """Assess contract risks using RAG."""
        risk_queries = [
            "What are the main risks and liabilities in this contract?",
            "What are the potential financial risks?",
            "What are the operational risks mentioned?",
            "What are the legal risks and potential disputes?"
        ]
        
        risk_assessment = {
            "financial_risks": [],
            "operational_risks": [],
            "legal_risks": [],
            "overall_risk_level": "Medium"
        }
        
        total_risk_score = 0
        
        for query in risk_queries:
            try:
                query_embedding = await self.llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                similar_chunks = await rag_store.retrieve_similar(
                    query_embedding[0], top_k=5, doc_id=doc_id
                )
                
                if similar_chunks:
                    context_chunks = [chunk.text for chunk, score in similar_chunks]
                    risk_analysis = await self.llm_adapter.generate_with_context(query, context_chunks)
                    
                    # Categorize risk
                    if "financial" in query.lower():
                        risk_assessment["financial_risks"].append(risk_analysis)
                        total_risk_score += 1
                    elif "operational" in query.lower():
                        risk_assessment["operational_risks"].append(risk_analysis)
                        total_risk_score += 1
                    elif "legal" in query.lower():
                        risk_assessment["legal_risks"].append(risk_analysis)
                        total_risk_score += 2  # Legal risks weighted higher
                        
            except Exception as e:
                print(f"Error assessing risks for query '{query}': {e}")
        
        # Determine overall risk level
        if total_risk_score >= 6:
            risk_assessment["overall_risk_level"] = "High"
        elif total_risk_score >= 3:
            risk_assessment["overall_risk_level"] = "Medium"
        else:
            risk_assessment["overall_risk_level"] = "Low"
        
        risk_assessment["total_risk_score"] = total_risk_score
        
        return risk_assessment
    
    @validate_input(
        doc_id=lambda x: bool(x and x.strip()),
        query=lambda x: bool(x and x.strip())
    )
    async def query_contract(self, doc_id: str, query: str, 
                           include_context: bool = True) -> Dict[str, Any]:
        """
        Query a specific contract using RAG.
        
        Args:
            doc_id: Document identifier
            query: Natural language query
            include_context: Whether to include context chunks in response
            
        Returns:
            Query response with relevant information
            
        Performance:
            Target: < 2 seconds for typical queries
            Timeout: 10 seconds maximum
        """
        operation_name = "query_contract"
        start_time = datetime.utcnow()
        correlation_id = str(uuid.uuid4())
        try:
            # Input validation
            if not doc_id or not doc_id.strip():
                error_msg = "Document ID is required"
                self.metrics.record_operation(
                    operation_name=operation_name,
                    success=False,
                    duration_ms=0,
                    error_type="VALIDATION_ERROR"
                )
                return {"error": error_msg}
            
            if not query or not query.strip():
                error_msg = "Query text is required"
                self.metrics.record_operation(
                    operation_name=operation_name,
                    success=False,
                    duration_ms=0,
                    error_type="VALIDATION_ERROR"
                )
                return {"error": error_msg}
            
            logger.info(f"Processing query for document {doc_id}", extra={
                "correlation_id": correlation_id,
                "doc_id": doc_id,
                "operation": operation_name
            })
            
            # Get query embedding
            query_embedding = await self.llm_adapter.get_embeddings([query])
            if not query_embedding:
                error_msg = "Failed to generate query embedding"
                self.metrics.record_operation(
                    operation_name=operation_name,
                    success=False,
                    duration_ms=(datetime.utcnow() - start_time).total_seconds() * 1000,
                    error_type="EMBEDDING_ERROR"
                )
                return {"error": error_msg}
            
            # Retrieve similar chunks
            similar_chunks = await rag_store.retrieve_similar(
                query_embedding[0], top_k=5, doc_id=doc_id
            )
            
            if not similar_chunks:
                # This is not an error, just no results found
                processing_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                self.metrics.record_operation(
                    operation_name=operation_name,
                    success=True,
                    duration_ms=processing_time_ms
                )
                return {
                    "answer": "No relevant information found in the contract for this query.",
                    "chunks": [],
                    "query": query,
                    "processing_time_ms": processing_time_ms
                }
            
            # Generate response using context
            context_chunks = [chunk.text for chunk, score in similar_chunks]
            answer = await self.llm_adapter.generate_with_context(query, context_chunks)
            
            # Calculate processing time
            processing_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record successful operation
            self.metrics.record_operation(
                operation_name=operation_name,
                success=True,
                duration_ms=processing_time_ms
            )
            
            response = {
                "answer": answer,
                "query": query,
                "total_chunks_retrieved": len(similar_chunks),
                "processing_time_ms": processing_time_ms
            }
            
            if include_context:
                chunk_details = []
                for chunk, score in similar_chunks:
                    chunk_details.append({
                        "id": chunk.id,
                        "text": chunk.text[:300] + "..." if len(chunk.text) > 300 else chunk.text,
                        "page": chunk.page,
                        "similarity_score": round(score, 3),
                        "start_pos": chunk.start_pos,
                        "end_pos": chunk.end_pos
                    })
                response["chunks"] = chunk_details
            
            logger.info(
                f"Query processed successfully for document {doc_id}",
                extra={
                    "correlation_id": correlation_id,
                    "doc_id": doc_id,
                    "operation": operation_name,
                    "duration_ms": processing_time_ms,
                    "chunks_retrieved": len(similar_chunks)
                }
            )
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            processing_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record error metrics
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=processing_time_ms,
                error_type=e.__class__.__name__
            )
            
            logger.error(
                error_msg,
                extra={
                    "correlation_id": correlation_id,
                    "doc_id": doc_id,
                    "operation": operation_name,
                    "error_type": e.__class__.__name__,
                    "duration_ms": processing_time_ms
                },
                exc_info=True
            )
            
            return {
                "error": error_msg,
                "processing_time_ms": processing_time_ms
            }
    
    @validate_input(
        doc_ids=lambda x: bool(x and len(x) > 0),
        comparison_criteria=lambda x: bool(x and len(x) > 0)
    )
    async def compare_contracts(self, doc_ids: List[str], 
                              comparison_criteria: List[str]) -> Dict[str, Any]:
        """
        Compare multiple contracts using RAG.
        
        Args:
            doc_ids: List of document identifiers
            comparison_criteria: List of criteria to compare
            
        Returns:
            Comparison results
            
        Performance:
            Target: < 5 seconds per document for typical comparisons
            Timeout: 30 seconds maximum
        """
        operation_name = "compare_contracts"
        start_time = datetime.utcnow()
        correlation_id = str(uuid.uuid4())
        try:
            # Input validation
            if not doc_ids:
                error_msg = "Document IDs list is required"
                self.metrics.record_operation(
                    operation_name=operation_name,
                    success=False,
                    duration_ms=0,
                    error_type="VALIDATION_ERROR"
                )
                return {"error": error_msg}
            
            if not comparison_criteria:
                error_msg = "Comparison criteria list is required"
                self.metrics.record_operation(
                    operation_name=operation_name,
                    success=False,
                    duration_ms=0,
                    error_type="VALIDATION_ERROR"
                )
                return {"error": error_msg}
            
            logger.info(
                f"Starting contract comparison for {len(doc_ids)} documents",
                extra={
                    "correlation_id": correlation_id,
                    "doc_count": len(doc_ids),
                    "criteria_count": len(comparison_criteria),
                    "operation": operation_name
                }
            )
            
            comparison_results = {}
            total_queries = 0
            successful_queries = 0
            
            for criterion in comparison_criteria:
                criterion_results = {}
                
                for doc_id in doc_ids:
                    try:
                        # Query each contract for the criterion
                        query = f"What are the {criterion} in this contract?"
                        total_queries += 1
                        result = await self.query_contract(doc_id, query, include_context=False)
                        
                        if "error" not in result:
                            successful_queries += 1
                            criterion_results[doc_id] = {
                                "answer": result.get("answer", "No information found"),
                                "chunks_retrieved": result.get("total_chunks_retrieved", 0),
                                "processing_time_ms": result.get("processing_time_ms", 0)
                            }
                        else:
                            criterion_results[doc_id] = {
                                "error": result["error"],
                                "chunks_retrieved": 0,
                                "processing_time_ms": result.get("processing_time_ms", 0)
                            }
                        
                    except Exception as e:
                        criterion_results[doc_id] = {
                            "error": str(e),
                            "chunks_retrieved": 0,
                            "processing_time_ms": 0
                        }
                
                comparison_results[criterion] = criterion_results
            
            # Calculate total processing time
            processing_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record metrics
            self.metrics.record_operation(
                operation_name=operation_name,
                success=True,
                duration_ms=processing_time_ms
            )
            
            logger.info(
                "Contract comparison completed",
                extra={
                    "correlation_id": correlation_id,
                    "doc_count": len(doc_ids),
                    "criteria_count": len(comparison_criteria),
                    "operation": operation_name,
                    "duration_ms": processing_time_ms,
                    "successful_queries": successful_queries,
                    "total_queries": total_queries
                }
            )
            
            return {
                "comparison_criteria": comparison_criteria,
                "documents_compared": doc_ids,
                "results": comparison_results,
                "processing_time_ms": processing_time_ms,
                "successful_queries": successful_queries,
                "total_queries": total_queries
            }
            
        except Exception as e:
            error_msg = f"Error comparing contracts: {str(e)}"
            processing_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record error metrics
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=processing_time_ms,
                error_type=e.__class__.__name__
            )
            
            logger.error(
                error_msg,
                extra={
                    "correlation_id": correlation_id,
                    "doc_count": len(doc_ids),
                    "criteria_count": len(comparison_criteria),
                    "operation": operation_name,
                    "error_type": e.__class__.__name__,
                    "duration_ms": processing_time_ms
                },
                exc_info=True
            )
            
            return {
                "error": error_msg,
                "processing_time_ms": processing_time_ms
            }
    
    @validate_input(
        doc_ids=lambda x: bool(x and len(x) > 0 and all(id.strip() for id in x))
    )
    async def batch_analyze_contracts(
        self,
        doc_ids: List[str],
        parallel_limit: int = 5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform batch analysis of multiple contracts using RAG capabilities.
        
        Args:
            doc_ids: List of document identifiers
            parallel_limit: Maximum number of parallel analyses
            metadata: Optional metadata to apply to all documents
            
        Returns:
            Batch analysis results with success rate and timing metrics
            
        Performance:
            Target: < 20 seconds per document
            Timeout: 60 seconds per document
            Batch size limit: 50 documents
        """
        operation_name = "batch_analyze"
        start_time = datetime.utcnow()
        correlation_id = str(uuid.uuid4())
        
        if len(doc_ids) > 50:
            error_msg = "Batch size exceeds limit of 50 documents"
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=0,
                error_type="VALIDATION_ERROR"
            )
            return {"error": error_msg}
        
        structured_log(
            logger,
            "info",
            f"Starting batch analysis of {len(doc_ids)} documents",
            correlation_id,
            operation_name,
            batch_size=len(doc_ids)
        )
        
        results = {
            "successful": [],
            "failed": [],
            "total_documents": len(doc_ids),
            "success_rate": 0.0,
            "total_processing_time_ms": 0,
            "avg_processing_time_ms": 0
        }
        
        try:
            import asyncio
            from asyncio import Semaphore
            
            sem = Semaphore(parallel_limit)

            async def analyze_with_semaphore(doc_id: str) -> Tuple[str, Dict[str, Any]]:
                """Run analysis for a single document under semaphore control.

                Each invocation acquires the shared semaphore before calling the
                actual analysis routine, ensuring no more than ``parallel_limit``
                tasks execute concurrently.
                """

                async with sem:
                    try:
                        result = await self.analyze_contract_with_rag(
                            doc_id, text="", metadata=metadata
                        )
                        return doc_id, {"success": True, "result": result}
                    except Exception as e:
                        return doc_id, {"success": False, "error": str(e)}

            # Create tasks for all documents
            tasks = [analyze_with_semaphore(doc_id) for doc_id in doc_ids]

            # Wait for all tasks to complete and collect their results
            completed = await asyncio.gather(*tasks)

            # Process results and build structured response
            for doc_id, result in completed:
                if result["success"]:
                    results["successful"].append({
                        "doc_id": doc_id,
                        "result": result["result"]
                    })
                else:
                    results["failed"].append({
                        "doc_id": doc_id,
                        "error": result["error"]
                    })
            
            # Calculate metrics
            end_time = datetime.utcnow()
            total_time_ms = (end_time - start_time).total_seconds() * 1000
            success_rate = len(results["successful"]) / len(doc_ids) * 100
            
            results.update({
                "success_rate": round(success_rate, 2),
                "total_processing_time_ms": round(total_time_ms, 2),
                "avg_processing_time_ms": round(total_time_ms / len(doc_ids), 2)
            })
            
            # Record metrics
            self.metrics.record_operation(
                operation_name=operation_name,
                success=True,
                duration_ms=total_time_ms
            )
            
            structured_log(
                logger,
                "info",
                f"Batch analysis completed with {success_rate:.2f}% success rate",
                correlation_id,
                operation_name,
                success_rate=success_rate,
                duration_ms=total_time_ms,
                successful_count=len(results["successful"]),
                failed_count=len(results["failed"])
            )
            
            return results
            
        except Exception as e:
            error_msg = f"Batch analysis failed: {str(e)}"
            end_time = datetime.utcnow()
            total_time_ms = (end_time - start_time).total_seconds() * 1000
            
            self.metrics.record_operation(
                operation_name=operation_name,
                success=False,
                duration_ms=total_time_ms,
                error_type=e.__class__.__name__
            )
            
            structured_log(
                logger,
                "error",
                error_msg,
                correlation_id,
                operation_name,
                error_type=e.__class__.__name__,
                duration_ms=total_time_ms,
                exc_info=True
            )
            
            return {
                "error": error_msg,
                "total_documents": len(doc_ids),
                "processing_time_ms": total_time_ms
            }
    
    @validate_input(
        doc_id=lambda x: bool(x and x.strip())
    )
    async def generate_summary_report(self, doc_id: str) -> Dict[str, Any]:
        """Generate a comprehensive summary report for a contract."""
        try:
            # Get document chunks
            chunks = rag_store.get_document_chunks(doc_id)
            if not chunks:
                return {"error": "Document not found or no chunks available"}
            
            # Generate comprehensive summary
            summary_queries = [
                "Provide a comprehensive executive summary of this contract",
                "What are the key terms and conditions?",
                "What are the main obligations of each party?",
                "What are the critical dates and deadlines?",
                "What are the key risks and considerations?"
            ]
            
            summary_sections = {}
            
            for query in summary_queries:
                try:
                    result = await self.query_contract(doc_id, query, include_context=False)
                    section_name = query.split(" of ")[-1].replace("?", "").lower()
                    summary_sections[section_name] = result.get("answer", "No information available")
                except Exception as e:
                    section_name = query.split(" of ")[-1].replace("?", "").lower()
                    summary_sections[section_name] = f"Error generating section: {str(e)}"
            
            return {
                "doc_id": doc_id,
                "total_chunks": len(chunks),
                "summary_sections": summary_sections,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error generating summary report: {str(e)}"}

# Global instance
rag_analyzer = RAGAnalyzer()
