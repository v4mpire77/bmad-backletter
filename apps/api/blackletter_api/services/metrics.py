"""Metrics service for Story 2.4 and Story 4.1"""
from __future__ import annotations

import logging
from typing import Dict, Any, List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, and_
from datetime import datetime, timedelta

from ..models.entities import Metric, Analysis
from ..database import engine
from ..services.llm_gate import get_llm_gate

logger = logging.getLogger(__name__)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MetricsService:
    """Service for computing and aggregating metrics."""
    
    def __init__(self):
        self.llm_gate = get_llm_gate()
    
    def get_admin_metrics(self) -> Dict[str, Any]:
        """
        Get admin metrics for Story 4.1 - Metrics Wall.
        
        Returns tiles data for:
        - p95 latency
        - tokens/doc 
        - %LLM usage
        - explainability rate
        """
        session = SessionLocal()
        try:
            # Get metrics for last 30 runs
            recent_metrics = session.query(Metric).order_by(
                Metric.created_at.desc()
            ).limit(30).all()
            
            if not recent_metrics:
                return self._empty_metrics()
            
            # Basic aggregations
            total_analyses = len(recent_metrics)
            total_tokens = sum(m.tokens_per_doc for m in recent_metrics)
            llm_invoked_count = sum(1 for m in recent_metrics if m.llm_invoked)
            
            # P95 latency (mock implementation - would need actual timing data)
            processing_times = [m.processing_time_ms for m in recent_metrics if m.processing_time_ms]
            p95_latency = self._calculate_percentile(processing_times, 95) if processing_times else 0
            
            # Tokens per doc
            avg_tokens_per_doc = round(total_tokens / total_analyses, 2) if total_analyses > 0 else 0
            
            # LLM usage percentage
            llm_usage_percent = round((llm_invoked_count / total_analyses) * 100, 2) if total_analyses > 0 else 0
            
            # Explainability rate (mock - would depend on actual implementation)
            explainability_rate = 85.5  # Placeholder
            
            return {
                "p95_latency_ms": round(p95_latency, 2),
                "avg_tokens_per_doc": avg_tokens_per_doc,
                "llm_usage_percent": llm_usage_percent,
                "explainability_rate": explainability_rate,
                "total_analyses": total_analyses,
                "hard_cap_limit": self.llm_gate.hard_cap,
                "cap_exceeded_count": sum(1 for m in recent_metrics if m.error_reason == 'token_cap')
            }
            
        except Exception as e:
            logger.error(f"Failed to get admin metrics: {e}")
            return self._empty_metrics()
        finally:
            session.close()
    
    def get_metrics_time_series(self, days: int = 30) -> Dict[str, List]:
        """
        Get time series data for sparkline charts.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Time series data for metrics visualization
        """
        session = SessionLocal()
        try:
            # Get metrics from last N days
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            metrics = session.query(Metric).filter(
                Metric.created_at >= cutoff_date
            ).order_by(Metric.created_at).all()
            
            if not metrics:
                return {"dates": [], "tokens": [], "llm_usage": [], "latency": []}
            
            # Group by day
            daily_data = {}
            for metric in metrics:
                day_key = metric.created_at.date().isoformat()
                if day_key not in daily_data:
                    daily_data[day_key] = {
                        "tokens": [],
                        "llm_invoked": [],
                        "processing_times": []
                    }
                
                daily_data[day_key]["tokens"].append(metric.tokens_per_doc)
                daily_data[day_key]["llm_invoked"].append(metric.llm_invoked)
                if metric.processing_time_ms:
                    daily_data[day_key]["processing_times"].append(metric.processing_time_ms)
            
            # Aggregate daily metrics
            dates = sorted(daily_data.keys())
            daily_tokens = []
            daily_llm_usage = []
            daily_latency = []
            
            for date in dates:
                data = daily_data[date]
                
                # Average tokens per day
                avg_tokens = sum(data["tokens"]) / len(data["tokens"]) if data["tokens"] else 0
                daily_tokens.append(round(avg_tokens, 2))
                
                # LLM usage percentage per day
                llm_percent = (sum(data["llm_invoked"]) / len(data["llm_invoked"]) * 100) if data["llm_invoked"] else 0
                daily_llm_usage.append(round(llm_percent, 2))
                
                # Average latency per day
                avg_latency = sum(data["processing_times"]) / len(data["processing_times"]) if data["processing_times"] else 0
                daily_latency.append(round(avg_latency, 2))
            
            return {
                "dates": dates,
                "tokens": daily_tokens,
                "llm_usage": daily_llm_usage,
                "latency": daily_latency
            }
            
        except Exception as e:
            logger.error(f"Failed to get time series metrics: {e}")
            return {"dates": [], "tokens": [], "llm_usage": [], "latency": []}
        finally:
            session.close()
    
    def record_analysis_completion(
        self, 
        analysis_id: str, 
        processing_time_ms: float,
        detection_count: int,
        tokens_used: int = 0,
        llm_invoked: bool = False,
        error_reason: str = None
    ) -> None:
        """
        Record completion metrics for an analysis.
        
        This would be called at the end of the detection pipeline.
        """
        session = SessionLocal()
        try:
            # Update or create metric record
            metric = session.query(Metric).filter(
                Metric.analysis_id == analysis_id
            ).first()
            
            if metric:
                # Update existing
                metric.processing_time_ms = processing_time_ms
                metric.detection_count = detection_count
                if tokens_used > 0:
                    metric.tokens_per_doc += tokens_used
                    metric.llm_invoked = metric.llm_invoked or llm_invoked
                if error_reason:
                    metric.error_reason = error_reason
            else:
                # Create new
                metric = Metric(
                    analysis_id=analysis_id,
                    tokens_per_doc=tokens_used,
                    llm_invoked=llm_invoked,
                    processing_time_ms=processing_time_ms,
                    detection_count=detection_count,
                    error_reason=error_reason
                )
                session.add(metric)
            
            session.commit()
            logger.info(f"Recorded completion metrics for analysis {analysis_id}")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to record completion metrics for {analysis_id}: {e}")
        finally:
            session.close()
    
    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate the specified percentile of a list of values."""
        if not values:
            return 0.0
            
        sorted_values = sorted(values)
        index = (percentile / 100.0) * (len(sorted_values) - 1)
        
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight
    
    def _empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics structure."""
        return {
            "p95_latency_ms": 0,
            "avg_tokens_per_doc": 0,
            "llm_usage_percent": 0,
            "explainability_rate": 0,
            "total_analyses": 0,
            "hard_cap_limit": self.llm_gate.hard_cap,
            "cap_exceeded_count": 0
        }


# Global instance
_metrics_service_instance: MetricsService = None


def get_metrics_service() -> MetricsService:
    """Get the global metrics service instance."""
    global _metrics_service_instance
    if _metrics_service_instance is None:
        _metrics_service_instance = MetricsService()
    return _metrics_service_instance