"""
LLM Adapter module for Blackletter Systems.

This module provides a simplified interface for OpenAI LLM provider.

Usage:
    from app.core.llm_adapter import generate
    
    # Generate text with OpenAI
    response = await generate(
        text="Summarize this contract",
        system="You are a legal assistant",
    )
    
    # Or specify a model
    response = await generate(
        text="Summarize this contract",
        system="You are a legal assistant",
        model="gpt-4o",
    )
"""

import os
from typing import Optional
import logging

# Import OpenAI library
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = "gpt-4o"

# Client instance
_openai_client = None

def _get_openai_client():
    """Get or initialize OpenAI client"""
    global _openai_client
    if _openai_client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        _openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    return _openai_client

async def generate(
    text: str, 
    system: str, 
    model: Optional[str] = None
) -> str:
    """
    Generate text using OpenAI.
    
    Args:
        text: The prompt text to send to the LLM
        system: The system prompt to guide the LLM
        model: Optional model name to use (defaults to gpt-4o)
        
    Returns:
        str: The generated text response
    
    Raises:
        ValueError: If the OpenAI API key is missing
        Exception: If there's an issue with the API request
    """
    client = _get_openai_client()
    model = model or DEFAULT_MODEL
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": text}
            ],
            temperature=0.1,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating text with OpenAI: {str(e)}")
        raise