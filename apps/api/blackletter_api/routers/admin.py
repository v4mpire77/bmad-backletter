from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..services.metrics import get_metrics_service
from ..services.llm_gate import get_llm_gate

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/metrics")
async def get_admin_metrics() -> Dict[str, Any]:
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
        
        # Format as tiles for frontend
        return {
            "tiles": {
                "p95_latency": {
                    "value": metrics["p95_latency_ms"],
                    "unit": "ms",
                    "label": "P95 Latency",
                    "status": "normal" if metrics["p95_latency_ms"] < 60000 else "warning"
                },
                "tokens_per_doc": {
                    "value": metrics["avg_tokens_per_doc"],
                    "unit": "tokens",
                    "label": "Tokens/Doc",
                    "status": "normal" if metrics["avg_tokens_per_doc"] < metrics["hard_cap_limit"] * 0.8 else "warning"
                },
                "llm_usage": {
                    "value": metrics["llm_usage_percent"],
                    "unit": "%",
                    "label": "%LLM Usage",
                    "status": "normal"
                },
                "explainability_rate": {
                    "value": metrics["explainability_rate"],
                    "unit": "%", 
                    "label": "Explainability Rate",
                    "status": "normal" if metrics["explainability_rate"] > 80 else "warning"
                }
            },
            "summary": {
                "total_analyses": metrics["total_analyses"],
                "hard_cap_limit": metrics["hard_cap_limit"],
                "cap_exceeded_count": metrics["cap_exceeded_count"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve admin metrics: {str(e)}")


@router.get("/metrics/timeseries")
async def get_metrics_timeseries(days: int = 30) -> Dict[str, Any]:
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
        
        return {
            "timeseries": timeseries,
            "metadata": {
                "days_requested": days,
                "data_points": len(timeseries.get("dates", [])),
                "last_updated": timeseries.get("dates", [])[-1] if timeseries.get("dates") else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve time series data: {str(e)}")


@router.get("/token-usage/{analysis_id}")
async def get_analysis_token_usage(analysis_id: str) -> Dict[str, Any]:
    """Get detailed token usage for a specific analysis."""
    try:
        llm_gate = get_llm_gate()
        current_usage = llm_gate.get_current_token_usage(analysis_id)
        
        return {
            "analysis_id": analysis_id,
            "tokens_per_doc": current_usage,
            "hard_cap_limit": llm_gate.hard_cap,
            "cap_exceeded": current_usage >= llm_gate.hard_cap,
            "usage_percentage": round((current_usage / llm_gate.hard_cap) * 100, 2) if llm_gate.hard_cap > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve token usage: {str(e)}")


@router.get("/metrics/aggregates")
async def get_aggregate_metrics() -> Dict[str, Any]:
    """Get aggregate metrics over last 30 runs."""
    try:
        llm_gate = get_llm_gate()
        analysis_metrics = llm_gate.get_analysis_metrics()
        
        return {
            "aggregates": analysis_metrics,
            "computed_at": "recent",
            "scope": "last_30_runs"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve aggregate metrics: {str(e)}")


@router.get("/health")
async def get_system_health() -> Dict[str, Any]:
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
                "functioning": True
            },
            "system": {
                "version": "1.0.0",
                "environment": "development"
            },
            "components": {
                "llm_gate": "operational",
                "metrics_service": "operational",
                "database": "connected"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "components": {
                "llm_gate": "error",
                "metrics_service": "error", 
                "database": "unknown"
            }
        }