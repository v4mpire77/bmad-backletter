"""LLM Gate Service for Story 2.4 - Token Ledger & Caps"""
from __future__ import annotations

import logging
from typing import Dict, Optional, Tuple
from ..core_config_loader import load_core_config
from ..models.entities import Metric
from ..database import engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class LLMGate:
    """
    LLM Gate adapter with token counters and hard cap enforcement.
    
    Enforces hard_cap_tokens_per_doc from core-config.yaml and records
    tokens_per_doc for every analysis.
    """
    
    def __init__(self):
        self.config = load_core_config()
        self.hard_cap = self.config.budget.hard_cap_tokens_per_doc
        self.on_exceed = self.config.budget.on_exceed
        
    def check_token_allowance(self, analysis_id: str, proposed_tokens: int) -> Tuple[bool, Optional[str]]:
        """
        Check if adding proposed_tokens would exceed the hard cap.
        
        Returns:
            (allowed: bool, reason: Optional[str])
        """
        current_usage = self.get_current_token_usage(analysis_id)
        projected_total = current_usage + proposed_tokens
        
        if projected_total > self.hard_cap:
            reason = f"token_cap: {projected_total} would exceed limit of {self.hard_cap}"
            logger.warning(f"Token cap exceeded for analysis {analysis_id}: {reason}")
            return False, reason
            
        return True, None
    
    def record_token_usage(
        self, 
        analysis_id: str, 
        tokens_used: int, 
        llm_invoked: bool = False,
        error_reason: Optional[str] = None
    ) -> None:
        """
        Record token usage in Metric table for an analysis.
        
        Args:
            analysis_id: Analysis ID
            tokens_used: Number of tokens consumed
            llm_invoked: Whether LLM was actually invoked
            error_reason: Error reason if cap exceeded or other issues
        """
        session = SessionLocal()
        try:
            # Get existing metric or create new one
            existing_metric = session.query(Metric).filter(
                Metric.analysis_id == analysis_id
            ).first()
            
            if existing_metric:
                # Update existing metric
                existing_metric.tokens_per_doc += tokens_used
                existing_metric.llm_invoked = existing_metric.llm_invoked or llm_invoked
                if error_reason:
                    existing_metric.error_reason = error_reason
                metric = existing_metric
            else:
                # Create new metric
                metric = Metric(
                    analysis_id=analysis_id,
                    tokens_per_doc=tokens_used,
                    llm_invoked=llm_invoked,
                    error_reason=error_reason
                )
                session.add(metric)
            
            session.commit()
            logger.info(f"Recorded {tokens_used} tokens for analysis {analysis_id}, LLM invoked: {llm_invoked}")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to record token usage for {analysis_id}: {e}")
        finally:
            session.close()
    
    def get_current_token_usage(self, analysis_id: str) -> int:
        """Get current token usage for an analysis."""
        session = SessionLocal()
        try:
            metric = session.query(Metric).filter(
                Metric.analysis_id == analysis_id
            ).first()
            
            return metric.tokens_per_doc if metric else 0
            
        except Exception as e:
            logger.error(f"Failed to get token usage for {analysis_id}: {e}")
            return 0
        finally:
            session.close()
    
    def enforce_cap_on_findings(self, analysis_id: str, findings: list) -> list:
        """
        When cap is exceeded, set incomplete findings to 'needs_review' status.
        
        Args:
            analysis_id: Analysis ID
            findings: List of detection findings
            
        Returns:
            Modified findings list with needs_review status where appropriate
        """
        current_usage = self.get_current_token_usage(analysis_id)
        
        if current_usage >= self.hard_cap:
            logger.warning(f"Cap exceeded for {analysis_id}, marking incomplete findings as needs_review")
            
            # Mark incomplete findings as needs_review
            for finding in findings:
                if finding.get('status') in ['pending', 'incomplete', None]:
                    finding['status'] = 'needs_review'
                    finding['reason'] = 'token_cap'
                    
        return findings
    
    def get_analysis_metrics(self) -> Dict:
        """
        Get aggregate metrics for admin display.
        
        Returns metrics for admin dashboard including:
        - tokens/doc average
        - %docs_invoking_LLM
        """
        session = SessionLocal()
        try:
            metrics = session.query(Metric).all()
            
            if not metrics:
                return {
                    "avg_tokens_per_doc": 0,
                    "percent_docs_invoking_llm": 0,
                    "total_analyses": 0,
                    "total_tokens": 0,
                    "cap_exceeded_count": 0
                }
            
            total_tokens = sum(m.tokens_per_doc for m in metrics)
            total_analyses = len(metrics)
            llm_invoked_count = sum(1 for m in metrics if m.llm_invoked)
            cap_exceeded_count = sum(1 for m in metrics if m.error_reason == 'token_cap')
            
            return {
                "avg_tokens_per_doc": round(total_tokens / total_analyses, 2),
                "percent_docs_invoking_llm": round((llm_invoked_count / total_analyses) * 100, 2),
                "total_analyses": total_analyses,
                "total_tokens": total_tokens,
                "cap_exceeded_count": cap_exceeded_count,
                "hard_cap_limit": self.hard_cap
            }
            
        except Exception as e:
            logger.error(f"Failed to get analysis metrics: {e}")
            return {}
        finally:
            session.close()


# Global instance
_llm_gate_instance: Optional[LLMGate] = None


def get_llm_gate() -> LLMGate:
    """Get the global LLM gate instance."""
    global _llm_gate_instance
    if _llm_gate_instance is None:
        _llm_gate_instance = LLMGate()
    return _llm_gate_instance


def simulate_llm_call(analysis_id: str, snippet: str, max_tokens: int = 220) -> Tuple[bool, str, int]:
    """
    Simulate LLM call with token counting for testing.
    
    Returns:
        (success: bool, response: str, tokens_used: int)
    """
    gate = get_llm_gate()
    
    # Estimate tokens (rough approximation: 4 chars per token)
    estimated_tokens = len(snippet) // 4 + 50  # Add response tokens
    
    # Check allowance
    allowed, reason = gate.check_token_allowance(analysis_id, estimated_tokens)
    
    if not allowed:
        gate.record_token_usage(analysis_id, 0, False, reason)
        return False, f"Token cap exceeded: {reason}", 0
    
    # Simulate successful LLM call
    gate.record_token_usage(analysis_id, estimated_tokens, True)
    
    return True, f"LLM response for snippet (length: {len(snippet)})", estimated_tokens