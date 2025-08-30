from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from ..services.document_qa import DocumentQAService
from ..models.schemas import QAResponse


class QuestionRequest(BaseModel):
    question: str
    chat_history: Optional[List[str]] = None
    mode: Optional[str] = "simple"


router = APIRouter(tags=["qa"])
service = DocumentQAService()


@router.post("/documents/{document_id}/qa", response_model=QAResponse)
async def document_question_answer(
    document_id: str, payload: QuestionRequest
) -> QAResponse:
    """Answer a question about a specific document using RAG."""
    mode = payload.mode or "simple"
    if mode == "citations":
        return await service.answer_with_citations(document_id, payload.question)
    if mode == "conversational":
        return await service.answer_with_history(
            document_id, payload.question, payload.chat_history
        )
    if mode == "hybrid":
        return await service.answer_hybrid(
            document_id, payload.question, payload.chat_history
        )
    # default simple
    return await service.answer_simple(document_id, payload.question)
