from datetime import datetime

from celery import shared_task
from tasks.models import Task


@shared_task
def update_task_status():
    """
    Обновление статуса задач
    """

    Task.objects.filter(completion_date__lte=datetime.now().date()).update(active=False)
