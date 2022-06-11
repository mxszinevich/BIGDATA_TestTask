import factory.django

from factory.django import DjangoModelFactory

from tasks.models import TaskFile


class TaskFileFactory(DjangoModelFactory):
    """
    Фабрика файла задачи
    """

    file = factory.django.FileField(filename="file.png")

    class Meta:
        model = TaskFile
