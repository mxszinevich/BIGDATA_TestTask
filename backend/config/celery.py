import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.task_default_queue = "base"

app.conf.task_routes = {"tasks.tasks.*": {"queue": "base"}}


app.conf.beat_schedule = {
    "update_task_status": {
        "task": "tasks.tasks.update_task_status",
        "schedule": crontab(minute=0, hour=0),
    },
}
