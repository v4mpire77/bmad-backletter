from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..services.token_ledger import get_token_ledger, TokenUsage

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/metrics")
async def get_admin_metrics() -> Dict[str, Any]:
    """Get admin metrics including token usage statistics."""
    try:
        ledger = get_token_ledger()
        all_usage = ledger.get_all_usage()

        # Calculate aggregate statistics
        total_analyses = len(all_usage)
        total_tokens_used = sum(usage.total_tokens for usage in all_usage.values())
        total_input_tokens = sum(usage.input_tokens for usage in all_usage.values())
        total_output_tokens = sum(usage.output_tokens for usage in all_usage.values())

        analyses_needing_review = sum(1 for usage in all_usage.values() if usage.needs_review)
        token_cap = ledger.get_token_cap()

        # Group by model usage
        model_usage = {}
        for usage in all_usage.values():
            if usage.model_name:
                if usage.model_name not in model_usage:
                    model_usage[usage.model_name] = {
                        "total_tokens": 0,
                        "analysis_count": 0,
                        "avg_tokens_per_analysis": 0
                    }
                model_usage[usage.model_name]["total_tokens"] += usage.total_tokens
                model_usage[usage.model_name]["analysis_count"] += 1

        # Calculate averages
        for model_stats in model_usage.values():
            if model_stats["analysis_count"] > 0:
                model_stats["avg_tokens_per_analysis"] = (
                    model_stats["total_tokens"] / model_stats["analysis_count"]
                )

        return {
            "token_usage": {
                "total_analyses": total_analyses,
                "total_tokens_used": total_tokens_used,
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "token_cap": token_cap,
                "utilization_rate": (total_tokens_used / (total_analyses * token_cap)) if total_analyses > 0 else 0,
                "analyses_needing_review": analyses_needing_review,
                "review_rate": (analyses_needing_review / total_analyses) if total_analyses > 0 else 0
            },
            "model_usage": model_usage,
            "recent_analyses": [
                {
                    "analysis_id": usage.analysis_id,
                    "total_tokens": usage.total_tokens,
                    "needs_review": usage.needs_review,
                    "review_reason": usage.review_reason,
                    "model_name": usage.model_name
                }
                for usage in sorted(
                    all_usage.values(),
                    key=lambda x: x.total_tokens,
                    reverse=True
                )[:10]  # Top 10 by token usage
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")


@router.get("/token-usage/{analysis_id}")
async def get_analysis_token_usage(analysis_id: str) -> Dict[str, Any]:
    """Get detailed token usage for a specific analysis."""
    try:
        ledger = get_token_ledger()
        usage = ledger.get_usage(analysis_id)

        return {
            "analysis_id": usage.analysis_id,
            "total_tokens": usage.total_tokens,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "model_name": usage.model_name,
            "needs_review": usage.needs_review,
            "review_reason": usage.review_reason,
            "token_cap": ledger.get_token_cap(),
            "cap_exceeded": usage.total_tokens >= ledger.get_token_cap()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve token usage: {str(e)}")


@router.get("/token-usage")
async def get_all_token_usage(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """Get paginated list of all token usage records."""
    try:
        ledger = get_token_ledger()
        all_usage = ledger.get_all_usage()

        # Sort by most recent (we don't have timestamps, so sort by analysis_id)
        sorted_usage = sorted(
            all_usage.values(),
            key=lambda x: x.analysis_id,
            reverse=True
        )

        # Apply pagination
        paginated_usage = sorted_usage[offset:offset + limit]

        return {
            "total_count": len(all_usage),
            "limit": limit,
            "offset": offset,
            "usage_records": [
                {
                    "analysis_id": usage.analysis_id,
                    "total_tokens": usage.total_tokens,
                    "input_tokens": usage.input_tokens,
                    "output_tokens": usage.output_tokens,
                    "model_name": usage.model_name,
                    "needs_review": usage.needs_review,
                    "review_reason": usage.review_reason
                }
                for usage in paginated_usage
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve token usage records: {str(e)}")


@router.get("/health")
async def get_system_health() -> Dict[str, Any]:
    """Get basic system health information."""
    try:
        ledger = get_token_ledger()
        all_usage = ledger.get_all_usage()

        return {
            "status": "healthy",
            "token_ledger": {
                "total_analyses_tracked": len(all_usage),
                "token_cap": ledger.get_token_cap(),
                "caching_enabled": True  # We have caching in the ledger
            },
            "system": {
                "version": "1.0.0",  # This could be dynamic
                "environment": "development"  # This could be from env
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }