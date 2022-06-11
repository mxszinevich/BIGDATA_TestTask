from django.db import models

from tasks.models import Task


class TaskFile(models.Model):
    """
    Фаил задачи
    """

    task = models.ForeignKey(
        Task, verbose_name="Задача", related_name="files", on_delete=models.CASCADE
    )
    file = models.FileField(verbose_name="Фаил")

    class Meta:
        verbose_name = "Фаил задачи"
        verbose_name_plural = "Файлы задачи"

    def __str__(self):
        return f"{self.task.title}: Файл #{self.id}"
