"""
Celery Application Configuration for Background Tasks
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "rankscope_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max for crawling
)

# Periodic task beat schedule stub
celery_app.conf.beat_schedule = {
    "daily-ranking-checks": {
        "task": "app.workers.tasks.run_scheduled_rankings",
        "schedule": crontab(hour=2, minute=0),  # Run daily at 02:00 AM UTC
    },
    "weekly-technical-audits": {
        "task": "app.workers.tasks.run_scheduled_audits",
        "schedule": crontab(day_of_week=0, hour=3, minute=0),  # Run Sundays at 03:00 AM UTC
    },
}
