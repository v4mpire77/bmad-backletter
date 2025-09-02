import time
import logging
from collections import defaultdict, deque
from typing import Deque, Dict

import numpy as np
from sklearn.ensemble import IsolationForest

from .security_config import security_config

logger = logging.getLogger(__name__)


class ThreatDetectionService:
    """Service providing basic ML-based threat detection.

    The service analyses request behaviour using an IsolationForest model. It
    maintains a rolling training window so the model adapts as new patterns are
    observed. Scores above the configured threshold are considered suspicious.
    """

    def __init__(self, threshold: float = None, max_history: int = 1000) -> None:
        self.threshold = threshold or security_config.THREAT_SCORE_THRESHOLD
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.trained = False
        self.training_data: Deque[np.ndarray] = deque(maxlen=max_history)
        # Track session history for behavioural analysis
        self.session_history: Dict[str, Deque] = defaultdict(lambda: deque(maxlen=50))

    def _feature_vector(
        self,
        client_ip: str,
        path: str,
        method: str,
        user_agent: str,
        payload_size: int,
        session_id: str,
        timestamp: float,
    ) -> np.ndarray:
        """Extract numeric features from request data."""
        history = self.session_history[session_id]
        interval = timestamp - history[-1][0] if history else 1.0
        path_length = len(path)
        ua_hash = hash(user_agent) % 1000
        method_hash = hash(method) % 10
        features = np.array(
            [interval, path_length, ua_hash, method_hash, float(payload_size)],
            dtype=float,
        )
        history.append((timestamp, features))
        return features

    def analyze_request(
        self,
        *,
        client_ip: str,
        path: str,
        method: str,
        user_agent: str,
        payload_size: int,
        session_id: str,
    ) -> float:
        """Return threat score for the request."""
        ts = time.time()
        feature = self._feature_vector(
            client_ip, path, method, user_agent, payload_size, session_id, ts
        )

        # Collect baseline training data until model is ready
        if not self.trained:
            self.training_data.append(feature)
            if len(self.training_data) >= 50:
                self.model.fit(np.vstack(self.training_data))
                self.trained = True
            return 0.0

        # Score request
        score = -float(self.model.decision_function([feature])[0])
        self.training_data.append(feature)

        # Periodically retrain to adapt to new behaviour
        if len(self.training_data) % 50 == 0:
            self.model.fit(np.vstack(self.training_data))

        if score >= self.threshold:
            logger.warning(
                "Suspicious behaviour detected from %s (session %s) on %s: score %.2f",
                client_ip,
                session_id,
                path,
                score,
            )
        return score


# Global instance
threat_detection_service = ThreatDetectionService()
