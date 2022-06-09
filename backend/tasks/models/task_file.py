from django.db import models

from tasks.models import Task


class TaskFile(models.Model):
    """
    Фаил задачи
    """

    task = models.ForeignKey(Task, verbose_name="Задача", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Фаил")

    class Meta:
        verbose_name = "Фаил задачи"
        verbose_name_plural = "Файлы задачи"
