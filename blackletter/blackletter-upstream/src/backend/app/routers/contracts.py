"""
Contracts router for Blackletter Systems.

This module provides API endpoints for contract analysis:
- Upload contracts
- Review contracts
- Generate redlines
"""

import os
import time
from typing import Any, Callable, Dict, List, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
import httpx

from app.models.schemas import (
    DocumentType, DocumentUploadRequest, DocumentUploadResponse,
    ContractReviewRequest, ContractReviewResponse
)
from app.core.storage import upload_file, generate_presigned_url
from app.services.contract_review import review_contract

router = APIRouter()


def schedule_background_task(
    background_tasks: BackgroundTasks, target: Callable, *args, **kwargs
) -> None:
    """Schedule a coroutine to run after the response is sent.

    Centralizing this helper keeps route handlers clean and allows future
    enhancements (like logging) in one place.
    """

    background_tasks.add_task(target, *args, **kwargs)

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_contract(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(DocumentType.CONTRACT),
    metadata: Optional[str] = Form(None)
):
    """
    Upload a contract document for analysis.
    
    Args:
        file: The contract file
        document_type: Type of document
        metadata: Optional JSON metadata
        
    Returns:
        DocumentUploadResponse: Upload response with document key
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
        
        # Upload file to storage
        document_key = await upload_file(
            file_data=file,
            filename=file.filename,
            folder="contracts",
            content_type=file.content_type,
            metadata=parsed_metadata
        )
        
        # Create response
        from datetime import datetime
        response = DocumentUploadResponse(
            document_key=document_key,
            document_type=document_type,
            upload_time=datetime.now(),
            metadata=parsed_metadata
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading contract: {str(e)}")

@router.post("/review", response_model=ContractReviewResponse)
async def review_contract_endpoint(
    request: ContractReviewRequest,
    background_tasks: BackgroundTasks
):
    """
    Review a contract document.
    
    Args:
        request: Contract review request
        
    Returns:
        ContractReviewResponse: Review response with results
    """
    try:
        # Start timing
        start_time = time.time()
        
        # Review the contract
        review_result = await review_contract(
            document_key=request.document_key,
            document_type=request.document_type,
            playbook=request.playbook,
            metadata=request.metadata
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create response
        response = ContractReviewResponse(
            document_key=request.document_key,
            summary_key=review_result["summary_key"],
            review_key=review_result["review_key"],
            redlined_key=review_result.get("redlined_key"),
            issues_count=review_result["issues_count"],
            processing_time=processing_time
        )
        
        # Queue webhook notification in the background using helper
        schedule_background_task(
            background_tasks,
            notify_contract_processed,
            document_key=request.document_key,
            review_result=review_result,
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reviewing contract: {str(e)}")

@router.get("/download/{file_key}")
async def download_contract_file(file_key: str):
    """
    Generate a download URL for a contract file.
    
    Args:
        file_key: The S3 key of the file
        
    Returns:
        Dict: Dictionary with download URL
    """
    try:
        # Generate a presigned URL
        url = generate_presigned_url(file_key, expires_in=3600)
        
        return {"url": url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating download URL: {str(e)}")

async def notify_contract_processed(document_key: str, review_result: Dict[str, Any]):
    """
    Send a webhook notification when a contract is processed.
    
    Args:
        document_key: The document key
        review_result: The review result
    """
    try:
        # Get n8n webhook URL from environment
        n8n_url = os.getenv("N8N_URL", "http://localhost:5678")
        webhook_path = "/webhook/contract-uploaded"
        webhook_url = f"{n8n_url}{webhook_path}"
        
        # Prepare webhook payload
        from datetime import datetime
        payload = {
            "event_type": "contract_processed",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "document_key": document_key,
                "summary_key": review_result["summary_key"],
                "review_key": review_result["review_key"],
                "redlined_key": review_result.get("redlined_key"),
                "issues_count": review_result["issues_count"]
            }
        }
        
        # Send webhook request
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
        
    except Exception as e:
        import logging
        logging.error(f"Error sending webhook notification: {str(e)}")
        # Don't raise exception, this is a background task
