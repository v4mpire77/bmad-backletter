"""
Blackletter GDPR Processor - Enhanced Celery Configuration
Context Engineering Framework v2.0.0 Compliant
Background job processing with Redis message broker
Integrated from v4mpire77/blackletter for async job processing
"""
from __future__ import annotations

import os
import logging
from celery import Celery
from celery.signals import worker_ready, worker_shutdown
from kombu import Queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Celery app with enhanced configuration
celery_app = Celery(
    "blackletter_gdpr_processor",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["blackletter_api.services.tasks"]
)

# Enhanced Celery configuration from v4mpire77/blackletter
celery_app.conf.update(
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task routing
    task_routes={
        "blackletter_api.services.tasks.process_contract_analysis": {"queue": "gdpr_analysis"},
        "blackletter_api.services.tasks.cleanup_task": {"queue": "maintenance"}
    },
    
    # Queue configuration
    task_default_queue="default",
    task_queues=(
        Queue("default"),
        Queue("gdpr_analysis"),
        Queue("maintenance")
    ),
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    task_track_started=True,
    
    # Result backend configuration
    result_expires=3600,  # 1 hour
    result_backend_transport_options={"visibility_timeout": 3600},
    
    # Task execution
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    task_reject_on_worker_lost=True,
)


@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    """Log when worker is ready."""
    logger.info("Celery worker ready for GDPR analysis tasks")


@worker_shutdown.connect  
def worker_shutdown_handler(sender=None, **kwargs):
    """Log when worker shuts down."""
    logger.info("Celery worker shutting down")
