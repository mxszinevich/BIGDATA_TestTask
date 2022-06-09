from django.db import models

from users.models import User


class Task(models.Model):
    """
    Модель задачи
    """

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    title = models.CharField(verbose_name="Название задачи", max_length=300)
    description = models.TextField(verbose_name="Описание задачи")
    completion_date = models.DateField(verbose_name="Дата завершения задачи")
    active = models.BooleanField(verbose_name="Активно", default=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
