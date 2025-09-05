"""Celery worker entrypoint.

This module exposes the Celery application used by the API service so that a
worker can be launched with::

    celery -A apps.worker.worker:celery worker

Importing ``blackletter_api.services.tasks`` ensures that the task definitions
are registered with the Celery application.
"""

from blackletter_api.services.celery_app import celery_app

# Register task definitions with the Celery application
import blackletter_api.services.tasks  # noqa: F401  (side effects)

celery = celery_app

if __name__ == "__main__":
    # Allow ``python apps/worker/worker.py`` for local development
    celery.worker_main()

