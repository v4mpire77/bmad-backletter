# Skeleton module illustrating framework best practices.

from datetime import datetime
from typing import Any, Dict
import logging


class ExampleError(Exception):
    """Custom exception for template usage."""


def example_function(param: str) -> Dict[str, Any]:
    """Example function showing logging, error handling, and performance metrics.

    Args:
        param: Example parameter.

    Returns:
        Example result dictionary.

    Raises:
        ExampleError: If processing fails.

    Performance:
        Target <100ms, timeout 1s.
    """
    start = datetime.utcnow()
    try:
        result = {"message": f"Received {param}"}
        duration_ms = (datetime.utcnow() - start).total_seconds() * 1000
        logging.info("example_function completed", extra={"duration_ms": duration_ms})
        return result
    except Exception as exc:  # pragma: no cover - template
        duration_ms = (datetime.utcnow() - start).total_seconds() * 1000
        logging.error("example_function failed", exc_info=True, extra={"duration_ms": duration_ms})
        raise ExampleError(str(exc)) from exc
