from __future__ import annotations

import os
from celery import Celery

celery_app = Celery(
    "blackletter_api",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)
