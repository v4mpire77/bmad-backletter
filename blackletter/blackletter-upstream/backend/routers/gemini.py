from fastapi import APIRouter, HTTPException, Depends
from ..app.core.auth import verify_supabase_jwt
from pydantic import BaseModel
import os
import google.generativeai as genai

router = APIRouter()

class GeminiChatRequest(BaseModel):
    prompt: str

class GeminiChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=GeminiChatResponse)
def chat_with_gemini(request: GeminiChatRequest, user=Depends(verify_supabase_jwt)):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in environment.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    try:
        result = model.generate_content(request.prompt)
        return GeminiChatResponse(response=result.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
