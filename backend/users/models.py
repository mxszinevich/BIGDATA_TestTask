from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Пользователь
    """

    REQUIRED_FIELDS = ["first_name", "last_name", "patronymic"]
    patronymic = models.CharField(verbose_name="Отчество", max_length=200, blank=True)

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self):
        """
        ФИО пользователя
        """

        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
