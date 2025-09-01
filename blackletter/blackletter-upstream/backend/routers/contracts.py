from fastapi import APIRouter, UploadFile, HTTPException
from pypdf import PdfReader
from io import BytesIO
import json
import re
import json
from ..app.core.llm_adapter import LLMAdapter
from ..models.schemas import ReviewResult

router = APIRouter()

# LLM Prompt templates (from COPILOT_INSTRUCTIONS)
SYSTEM_PROMPT = (
    "You are a UK legal assistant helping with quick, non-binding contract triage. Be concise."
)
USER_PROMPT = (
    "Return ONLY valid JSON (no commentary, no code fences, no explanation).\n"
    "Output a single JSON object with keys: summary (string), risks (array of strings).\n"
    "If information is missing, still return an object but note missing sections as empty or an explanatory string.\n"
    "Text: {text}"
)

# Adapter (async interface in app.core.llm_adapter)
llm = LLMAdapter()


@router.post("/review", response_model=ReviewResult)
async def review_contract(file: UploadFile):
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        # Read file content
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        # Extract text from PDF
        pdf = PdfReader(BytesIO(content))
        text_parts = []
        for page in pdf.pages:
            t = page.extract_text() or ""
            text_parts.append(t)
        text = "\n\n".join(text_parts).strip()

        if not text:
            raise HTTPException(status_code=400, detail="No extractable text found in PDF")

        # Truncate text to safe length for LLM
        truncated = text[:6000] + ("..." if len(text) > 6000 else "")

        # Call the adapter's analyze_contract (async)
        resp = await llm.analyze_contract(truncated)

        # Normalise response to text or dict
        if isinstance(resp, dict):
            parsed = resp
            summary = parsed.get("summary") or parsed.get("summary_text") or ""
            risks = parsed.get("risks") or parsed.get("issues") or []
            if isinstance(risks, str):
                risks = [risks]
        else:
            resp_text = str(resp)
            # 1) Try direct JSON
            parsed = None
            try:
                parsed = json.loads(resp_text)
            except Exception:
                parsed = None

            # 2) If not, try to extract JSON inside triple-backtick fences ```{...}```
            if parsed is None:
                m = re.search(r'```\s*({[\s\S]*?})\s*```', resp_text)
                if m:
                    try:
                        parsed = json.loads(m.group(1))
                    except Exception:
                        parsed = None

            # 3) If still not, try any {...} blocks (prefer the longest candidate)
            if parsed is None:
                candidates = re.findall(r'({[\s\S]*})', resp_text)
                candidates.sort(key=len, reverse=True)
                for cand in candidates:
                    try:
                        parsed = json.loads(cand)
                        break
                    except Exception:
                        # Try unescaping common backslash-escaped sequences
                        try:
                            unescaped = bytes(cand, "utf-8").decode("unicode_escape")
                            parsed = json.loads(unescaped)
                            break
                        except Exception:
                            # Try trimming surrounding quotes if present
                            try:
                                trimmed = cand.strip('"\'')
                                parsed = json.loads(trimmed)
                                break
                            except Exception:
                                parsed = None

            # 4) Final fallback: naive human-readable parsing
            if parsed is not None:
                summary = parsed.get("summary") or parsed.get("summary_text") or ""
                risks = parsed.get("risks") or parsed.get("issues") or []
                if isinstance(risks, str):
                    risks = [risks]
                # Coerce risk items to strings (handle dicts returned by some LLMs)
                coerced = []
                for r in risks:
                    if isinstance(r, str):
                        coerced.append(r)
                    elif isinstance(r, dict):
                        text = r.get("text") or r.get("description") or r.get("value")
                        if isinstance(text, str) and text:
                            coerced.append(text)
                        else:
                            try:
                                coerced.append(json.dumps(r))
                            except Exception:
                                coerced.append(str(r))
                    else:
                        coerced.append(str(r))
                risks = coerced
            else:
                # Fallback: naive split
                parts = [p.strip() for p in resp_text.split("\n\n") if p.strip()]
                summary = parts[0] if parts else ""
                risks = []
                for p in parts[1:]:
                    for line in p.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("-") or line.startswith("*"):
                            risks.append(line.lstrip("-* "))
                        else:
                            risks.append(line)

        return ReviewResult(summary=summary or "", risks=risks)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
