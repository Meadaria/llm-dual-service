from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "bot_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    result_expires=3600,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.autodiscover_tasks(["app.tasks"])