from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models.schemas import AnswerResponse, QuestionRequest
from ..services import qna_service

router = APIRouter(tags=["qna"])


@router.post("/documents/{document_id}/qa", response_model=AnswerResponse)
async def document_qna(document_id: str, payload: QuestionRequest) -> AnswerResponse:
    """Answer a question about a registered document."""
    if document_id not in qna_service.DOCUMENT_STORE:
        raise HTTPException(status_code=404, detail="document_not_found")
    answer = qna_service.answer_question(document_id, payload.question)
    return AnswerResponse(answer=answer)

