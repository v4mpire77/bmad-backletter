from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from ..services.metrics import get_metrics_service
from ..services.llm_gate import get_llm_gate
from apps.api.dependencies.auth import require_role
from apps.api.models.user import Role


class MetricTile(BaseModel):
    value: float
    unit: str
    label: str
    status: str


class MetricsTiles(BaseModel):
    p95_latency: MetricTile
    tokens_per_doc: MetricTile
    llm_usage: MetricTile
    explainability_rate: MetricTile


class MetricsSummary(BaseModel):
    total_analyses: int
    hard_cap_limit: int
    cap_exceeded_count: int


class AdminMetricsResponse(BaseModel):
    tiles: MetricsTiles
    summary: MetricsSummary


class TimeSeriesData(BaseModel):
    dates: List[str]
    tokens: List[float]
    llm_usage: List[float]
    latency: List[float]


class TimeSeriesMetadata(BaseModel):
    days_requested: int
    data_points: int
    last_updated: Optional[str]


class MetricsTimeSeriesResponse(BaseModel):
    timeseries: TimeSeriesData
    metadata: TimeSeriesMetadata


class TokenUsageResponse(BaseModel):
    analysis_id: str
    tokens_per_doc: int
    hard_cap_limit: int
    cap_exceeded: bool
    usage_percentage: float


class AggregateMetrics(BaseModel):
    avg_tokens_per_doc: float
    percent_docs_invoking_llm: float
    total_analyses: int
    total_tokens: int
    cap_exceeded_count: int
    hard_cap_limit: int


class AggregateMetricsResponse(BaseModel):
    aggregates: AggregateMetrics
    computed_at: str
    scope: str


router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_role(Role.ADMIN))],
)


@router.get("/metrics", response_model=AdminMetricsResponse)
async def get_admin_metrics() -> AdminMetricsResponse:
    """
    Story 4.1 - Get admin metrics tiles.

    Returns key metrics tiles:
    - p95 latency
    - tokens/doc
    - %LLM usage
    - explainability rate
    """
    try:
        metrics_service = get_metrics_service()
        metrics = metrics_service.get_admin_metrics()

        tiles = MetricsTiles(
            p95_latency=MetricTile(
                value=metrics["p95_latency_ms"],
                unit="ms",
                label="P95 Latency",
                status="normal" if metrics["p95_latency_ms"] < 60000 else "warning",
            ),
            tokens_per_doc=MetricTile(
                value=metrics["avg_tokens_per_doc"],
                unit="tokens",
                label="Tokens/Doc",
                status="normal" if metrics["avg_tokens_per_doc"] < metrics["hard_cap_limit"] * 0.8 else "warning",
            ),
            llm_usage=MetricTile(
                value=metrics["llm_usage_percent"],
                unit="%",
                label="%LLM Usage",
                status="normal",
            ),
            explainability_rate=MetricTile(
                value=metrics["explainability_rate"],
                unit="%",
                label="Explainability Rate",
                status="normal" if metrics["explainability_rate"] > 80 else "warning",
            ),
        )

        summary = MetricsSummary(
            total_analyses=metrics["total_analyses"],
            hard_cap_limit=metrics["hard_cap_limit"],
            cap_exceeded_count=metrics["cap_exceeded_count"],
        )

        return AdminMetricsResponse(tiles=tiles, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve admin metrics: {str(e)}")


@router.get("/metrics/timeseries", response_model=MetricsTimeSeriesResponse)
async def get_metrics_timeseries(days: int = 30) -> MetricsTimeSeriesResponse:
    """
    Story 4.1 - Get time series data for sparkline charts.

    Args:
        days: Number of days to look back (default 30)

    Returns:
        Time series data for metrics visualization
    """
    try:
        metrics_service = get_metrics_service()
        timeseries = metrics_service.get_metrics_time_series(days)

        return MetricsTimeSeriesResponse(
            timeseries=TimeSeriesData(**timeseries),
            metadata=TimeSeriesMetadata(
                days_requested=days,
                data_points=len(timeseries.get("dates", [])),
                last_updated=timeseries.get("dates", [])[-1] if timeseries.get("dates") else None,
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve time series data: {str(e)}")


@router.get("/token-usage/{analysis_id}", response_model=TokenUsageResponse)
async def get_analysis_token_usage(analysis_id: str) -> TokenUsageResponse:
    """Get detailed token usage for a specific analysis."""
    try:
        llm_gate = get_llm_gate()
        current_usage = llm_gate.get_current_token_usage(analysis_id)

        return TokenUsageResponse(
            analysis_id=analysis_id,
            tokens_per_doc=current_usage,
            hard_cap_limit=llm_gate.hard_cap,
            cap_exceeded=current_usage >= llm_gate.hard_cap,
            usage_percentage=round((current_usage / llm_gate.hard_cap) * 100, 2) if llm_gate.hard_cap > 0 else 0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve token usage: {str(e)}")


@router.get("/metrics/aggregates", response_model=AggregateMetricsResponse)
async def get_aggregate_metrics() -> AggregateMetricsResponse:
    """Get aggregate metrics over last 30 runs."""
    try:
        llm_gate = get_llm_gate()
        analysis_metrics = llm_gate.get_analysis_metrics()

        return AggregateMetricsResponse(
            aggregates=AggregateMetrics(**analysis_metrics),
            computed_at="recent",
            scope="last_30_runs",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve aggregate metrics: {str(e)}")


@router.get("/health")
async def get_system_health() -> dict:
    """Get basic system health information."""
    try:
        metrics_service = get_metrics_service()
        llm_gate = get_llm_gate()

        # Get basic health metrics
        admin_metrics = metrics_service.get_admin_metrics()

        return {
            "status": "healthy",
            "metrics_service": {
                "total_analyses_tracked": admin_metrics["total_analyses"],
                "token_cap": admin_metrics["hard_cap_limit"],
                "functioning": True,
            },
            "system": {
                "version": "1.0.0",
                "environment": "development",
            },
            "components": {
                "llm_gate": "operational",
                "metrics_service": "operational",
                "database": "connected",
            },
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "components": {
                "llm_gate": "error",
                "metrics_service": "error",
                "database": "unknown",
            },
        }

