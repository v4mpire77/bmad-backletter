import os
from celery import Celery

celery = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)
celery.conf.task_routes = {"tasks.*": {"queue": "default"}}

@celery.task(name="tasks.ping")
def ping():
    return "pong"
