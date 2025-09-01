"""FastAPI application exposing RAG capabilities.

The module provides a small API surface area that demonstrates how the
retrieval and generation utilities can be orchestrated.  The endpoints are
light‑weight and primarily intended for unit testing; they return mock data
but exercise the request/response shapes used by the real service.

In this commit we extend the API with several advanced features:

* **Batch processing** – ability to answer multiple questions in a single
  request.
* **Advanced search filters** – ``ruleset`` and ``severity`` filters are
  forwarded to the underlying retrieval module.
* **Export/reporting** – retrieval results can be exported as JSON or CSV.
* **Analytics tracking** – basic in‑memory counters for each endpoint.
"""

from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from .analytics import tracker
from .query import retrieve
from .reporting import results_to_csv

app = FastAPI(title="Blackletter RAG API")


class QARequest(BaseModel):
    """A question to be answered with optional retrieval filters."""

    question: str
    contract_id: Optional[str] = None
    ruleset: Optional[str] = None
    severity: Optional[str] = None


class Citation(BaseModel):
    source: str
    url: str


class QAResponse(BaseModel):
    answer: str
    citations: List[Citation]


class BatchQARequest(BaseModel):
    """Container for processing multiple questions at once."""

    questions: List[QARequest]


class BatchQAResponse(BaseModel):
    responses: List[QAResponse]


class ExplainRequest(BaseModel):
    finding_id: str


class ExplainResponse(BaseModel):
    reasoning: str
    citations: List[Citation]


@app.post("/rag/qa", response_model=QAResponse)
async def rag_qa(req: QARequest) -> QAResponse:
    """Answer a free‑text question using RAG."""

    tracker.record("qa")
    return QAResponse(
        answer=f"Mock answer for: {req.question}",
        citations=[Citation(source="Example Citation", url="https://example.com")],
    )


@app.post("/rag/batch-qa", response_model=BatchQAResponse)
async def rag_batch_qa(req: BatchQARequest) -> BatchQAResponse:
    """Process multiple questions in one request."""

    tracker.record("batch_qa")
    responses = [await rag_qa(q) for q in req.questions]
    return BatchQAResponse(responses=responses)


@app.post("/rag/export")
async def rag_export(req: QARequest, format: str = "json"):
    """Export retrieval results as JSON or CSV."""

    tracker.record("export")
    data = retrieve(
        req.question,
        contract_id=req.contract_id,
        ruleset=req.ruleset,
        severity=req.severity,
    )
    if format == "csv":
        csv_data = results_to_csv(data.get("results", []))
        return StreamingResponse(iter([csv_data]), media_type="text/csv")
    return JSONResponse(content=data)


@app.get("/rag/analytics")
async def rag_analytics() -> Dict[str, int]:
    """Return a snapshot of recorded analytics counters."""

    return tracker.snapshot()


@app.post("/rag/explain-finding", response_model=ExplainResponse)
async def rag_explain(req: ExplainRequest) -> ExplainResponse:
    """Provide reasoning and citations for a finding."""

    tracker.record("explain")
    return ExplainResponse(
        reasoning=f"Mock reasoning for finding {req.finding_id}",
        citations=[Citation(source="Example Citation", url="https://example.com")],
    )
