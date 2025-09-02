from __future__ import annotations

from typing import List

from ..models.schemas import Rulepack, Finding
from .detector_engine import evaluate
from ..core.verdict_mapper import map_verdict


def run_analysis(text: str, rulepack: Rulepack) -> List[Finding]:
    """Run detectors sequentially and aggregate findings.

    Detectors are executed in a deterministic order (sorted by ID).
    Failures in individual detectors produce a needs_review finding.
    """
    findings: List[Finding] = []
    for det in sorted(rulepack.detectors, key=lambda d: d.id):
        try:
            flags = evaluate(text, det, rulepack)
            verdict, confidence = map_verdict(
                flags["anchor"], flags["weak"], flags["redflag"]
            )
            findings.append(
                Finding(
                    detector_id=det.id,
                    rule_id=det.id,
                    verdict=verdict,
                    snippet=text,
                    page=1,
                    start=0,
                    end=len(text),
                    rationale="auto-evaluated",
                    confidence=confidence,
                )
            )
        except Exception as exc:  # pragma: no cover - simple safeguard
            findings.append(
                Finding(
                    detector_id=det.id,
                    rule_id=det.id,
                    verdict="needs_review",
                    snippet="",
                    page=1,
                    start=0,
                    end=0,
                    rationale=f"detector error: {exc}",
                    confidence=0.0,
                )
            )
    return findings
