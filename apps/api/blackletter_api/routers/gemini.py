"""
Gemini AI Router for contract analysis endpoints
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ..services.gemini_service import gemini_service, GeminiAnalysisResult, GeminiChatResponse
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gemini", tags=["gemini-ai"])


# Pydantic models for request/response
class ContractAnalysisRequest(BaseModel):
    """Request model for contract analysis"""
    contract_text: str = Field(..., min_length=10, description="The contract text to analyze")
    analysis_type: str = Field("general", description="Type of analysis: general, risk, compliance, financial")
    include_raw_response: bool = Field(False, description="Include raw Gemini response in output")


class ContractSummaryRequest(BaseModel):
    """Request model for contract summarization"""
    contract_text: str = Field(..., min_length=10, description="The contract text to summarize")
    max_length: int = Field(500, description="Maximum length of summary in words")


class ChatRequest(BaseModel):
    """Request model for AI chat"""
    message: str = Field(..., min_length=1, description="User's question or message")
    contract_context: Optional[str] = Field(None, description="Optional contract text for context")


class GeminiAnalysisResponse(BaseModel):
    """Response model for Gemini analysis"""
    summary: str
    key_terms: list[str]
    risk_factors: list[str]
    recommendations: list[str]
    confidence_score: float
    analysis_type: str
    raw_response: Optional[Dict[str, Any]] = None


class GeminiSummaryResponse(BaseModel):
    """Response model for contract summarization"""
    summary: str
    original_length: int
    summary_length: int


class GeminiChatResponseModel(BaseModel):
    """Response model for AI chat"""
    response: str
    suggestions: list[str]
    follow_up_questions: list[str]


class ServiceStatusResponse(BaseModel):
    """Response model for service status"""
    available: bool
    model: Optional[str] = None
    message: str


@router.get("/status", response_model=ServiceStatusResponse)
async def get_gemini_status():
    """Check if Gemini service is available and configured"""
    if not gemini_service.is_available():
        return ServiceStatusResponse(
            available=False,
            model=None,
            message="Gemini service not available. Please configure GEMINI_API_KEY in environment variables."
        )

    return ServiceStatusResponse(
        available=True,
        model=settings.gemini_model,
        message=f"Gemini service is available using model: {settings.gemini_model}"
    )


@router.post("/analyze-contract", response_model=GeminiAnalysisResponse)
async def analyze_contract(request: ContractAnalysisRequest):
    """
    Analyze contract text using Gemini AI

    Supports different analysis types:
    - general: Overall contract analysis
    - risk: Risk assessment and mitigation
    - compliance: GDPR and legal compliance
    - financial: Financial implications and commitments
    """
    if not gemini_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available. Please configure GEMINI_API_KEY."
        )

    # Validate analysis type
    valid_types = ["general", "risk", "compliance", "financial"]
    if request.analysis_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid analysis type. Must be one of: {', '.join(valid_types)}"
        )

    try:
        logger.info(f"Starting {request.analysis_type} analysis for contract (length: {len(request.contract_text)})")

        # Perform analysis
        result = gemini_service.analyze_contract(
            contract_text=request.contract_text,
            analysis_type=request.analysis_type
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to analyze contract. Please try again."
            )

        response = GeminiAnalysisResponse(
            summary=result.summary,
            key_terms=result.key_terms,
            risk_factors=result.risk_factors,
            recommendations=result.recommendations,
            confidence_score=result.confidence_score,
            analysis_type=request.analysis_type,
            raw_response=result.raw_response if request.include_raw_response else None
        )

        logger.info(f"Analysis completed successfully with confidence: {result.confidence_score}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during contract analysis: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during analysis"
        )


@router.post("/summarize-contract", response_model=GeminiSummaryResponse)
async def summarize_contract(request: ContractSummaryRequest):
    """Generate a concise summary of the contract using Gemini AI"""
    if not gemini_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available. Please configure GEMINI_API_KEY."
        )

    try:
        logger.info(f"Starting contract summarization (max_length: {request.max_length})")

        summary = gemini_service.summarize_contract(
            contract_text=request.contract_text,
            max_length=request.max_length
        )

        if not summary:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate summary. Please try again."
            )

        response = GeminiSummaryResponse(
            summary=summary,
            original_length=len(request.contract_text),
            summary_length=len(summary.split())
        )

        logger.info(f"Summary generated successfully ({response.summary_length} words)")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during contract summarization: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during summarization"
        )


@router.post("/chat", response_model=GeminiChatResponseModel)
async def chat_with_gemini(request: ChatRequest):
    """Interactive chat about contract-related questions using Gemini AI"""
    if not gemini_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available. Please configure GEMINI_API_KEY."
        )

    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")

        chat_response = gemini_service.chat_about_contract(
            message=request.message,
            contract_context=request.contract_context
        )

        if not chat_response:
            raise HTTPException(
                status_code=500,
                detail="Failed to process chat request. Please try again."
            )

        response = GeminiChatResponseModel(
            response=chat_response.response,
            suggestions=chat_response.suggestions,
            follow_up_questions=chat_response.follow_up_questions
        )

        logger.info("Chat request processed successfully")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during chat processing"
        )


@router.post("/analyze-contract-async")
async def analyze_contract_async(
    request: ContractAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze contract asynchronously (for large contracts)
    Returns job ID for status tracking
    """
    if not gemini_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available. Please configure GEMINI_API_KEY."
        )

    # This would integrate with the existing job system
    # For now, return a placeholder response
    job_id = f"gemini_analysis_{hash(request.contract_text) % 10000}"

    # Add to background tasks (would need proper job queue implementation)
    background_tasks.add_task(
        _process_async_analysis,
        job_id,
        request.contract_text,
        request.analysis_type,
        request.include_raw_response
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Analysis job queued for processing",
        "estimated_time": "30-60 seconds"
    }


async def _process_async_analysis(
    job_id: str,
    contract_text: str,
    analysis_type: str,
    include_raw: bool
):
    """Background task for async contract analysis"""
    try:
        logger.info(f"Starting async analysis job: {job_id}")

        # Perform analysis
        result = gemini_service.analyze_contract(contract_text, analysis_type)

        if result:
            logger.info(f"Async analysis completed: {job_id}")
            # Would store result in database/cache for retrieval
        else:
            logger.error(f"Async analysis failed: {job_id}")

    except Exception as e:
        logger.error(f"Error in async analysis {job_id}: {e}")


@router.get("/job/{job_id}")
async def get_analysis_job_status(job_id: str):
    """Get status of async analysis job"""
    # Placeholder - would integrate with job tracking system
    return {
        "job_id": job_id,
        "status": "completed",  # Would be dynamic
        "progress": 100,
        "message": "Analysis completed successfully"
    }


# Health check endpoint
@router.get("/health")
async def gemini_health_check():
    """Health check for Gemini service"""
    if not gemini_service.is_available():
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Gemini API key not configured"}
        )

    return {"status": "healthy", "model": settings.gemini_model}
