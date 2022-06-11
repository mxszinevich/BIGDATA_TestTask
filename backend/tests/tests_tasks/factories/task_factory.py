import datetime

from factory import Faker
from factory.django import DjangoModelFactory

from tasks.models import Task


class TaskFactory(DjangoModelFactory):
    """
    Фабрика задачи
    """

    title = Faker("word")
    description = Faker("paragraph")
    completion_date = datetime.datetime.now().date()

    class Meta:
        model = Task
