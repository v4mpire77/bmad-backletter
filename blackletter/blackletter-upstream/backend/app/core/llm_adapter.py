import os
import json
import asyncio
from typing import Optional, Any

try:
    import openai
except Exception:
    openai = None

try:
    import ollama
except Exception:
    ollama = None

import requests


class LLMAdapter:
    """Async adapter supporting OpenAI and Ollama (HTTP fallback).

    It prefers OpenAI when LLM_PROVIDER=openai and OPENAI_API_KEY is set. For Ollama it will
    try the python package then fall back to the HTTP API at OLLAMA_BASE_URL.
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = os.getenv("DEFAULT_LLM", "llama3.1:8b" if self.provider == "ollama" else "gpt-4")
        self.ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        if self.provider == "openai" and openai is not None:
            key = os.getenv("OPENAI_API_KEY")
            if key:
                openai.api_key = key

    async def _call_openai(self, messages: list) -> str:
        if openai is None:
            raise RuntimeError("openai package not available")
        # run in thread to avoid blocking event loop
        def sync_call():
            # Support both new OpenAI and older ChatCompletion shapes
            resp = None
            create = getattr(openai, "ChatCompletion", None)
            if create is not None:
                resp = create.create(model=self.model, messages=messages)
                # Try different access patterns
                if hasattr(resp, "choices"):
                    choice = resp.choices[0]
                    if hasattr(choice, "message"):
                        return getattr(choice.message, "content", "")
                    return getattr(choice, "text", "")

            # Fallback to chat completions via client method
            try:
                client_chat = getattr(openai, "chat", None)
                if client_chat is not None and hasattr(client_chat, "completions"):
                    resp = client_chat.completions.create(model=self.model, messages=messages)
                    if resp and hasattr(resp, "choices"):
                        return getattr(resp.choices[0].message, "content", "")
            except Exception:
                pass

            # Last resort: stringify whatever we have
            return str(resp or "")

        return await asyncio.to_thread(sync_call)

    async def _call_ollama(self, messages: list) -> str:
        # Prefer python client if available
        if ollama is not None:
            def sync_call():
                # use getattr to avoid static lint errors
                chat_fn = getattr(ollama, "chat", None)
                if chat_fn is not None:
                    res = chat_fn(model=self.model, messages=messages)
                    # handle different shapes
                    if isinstance(res, dict) and "message" in res:
                        return res["message"].get("content", "")
                    # try common attributes
                    if hasattr(res, "text"):
                        return getattr(res, "text")
                    return str(res)

                # try alternate client shape (guarded)
                chat_client_cls = getattr(ollama, "ChatClient", None)
                if callable(chat_client_cls):
                    try:
                        client = chat_client_cls()
                        if hasattr(client, "chat"):
                            res = getattr(client, "chat")(model=self.model, messages=messages)
                            return str(res)
                    except Exception:
                        pass

                return ""

            return await asyncio.to_thread(sync_call)

        # Fallback to HTTP
        url = self.ollama_base.rstrip("/") + "/api/chat"
        resp = requests.post(url, json={"model": self.model, "messages": messages}, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        if isinstance(body, dict):
            if "response" in body:
                return body["response"]
            if "choices" in body and body["choices"]:
                choice = body["choices"][0]
                if isinstance(choice, dict):
                    return choice.get("message", {}).get("content", "") or choice.get("content", "")
        return json.dumps(body)

    async def analyze_contract(self, text: str) -> Any:
        """Analyze contract text and return either parsed JSON or raw text."""
        prompt = (
            "Analyze this contract text and provide:\n"
            "1. A brief summary (2-3 sentences)\n"
            "2. Key risks or concerns\n"
            "3. Important dates or deadlines\n\n"
            "Format as JSON with keys: summary (string), risks (list), dates (list).\n"
        )

        system = "You are a legal contract analysis assistant. Be concise and focus on material risks."
        user = f"{prompt}\nText: {text}"
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

        if self.provider == "openai":
            resp = await self._call_openai(messages)
        else:
            resp = await self._call_ollama(messages)

        # Attempt to parse JSON
        try:
            return json.loads(resp)
        except Exception:
            return resp

