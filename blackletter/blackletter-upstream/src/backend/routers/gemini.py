from __future__ import annotations

import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()  # only needed locally

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def ask_gemini(prompt: str):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in environment")
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY,
    }
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=body)
    return response.json()


router = APIRouter()


class GeminiRequest(BaseModel):
    prompt: str


@router.post("/gemini")
def generate(req: GeminiRequest):
    return ask_gemini(req.prompt)

