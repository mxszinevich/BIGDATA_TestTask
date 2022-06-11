from rest_framework.serializers import ModelSerializer, FileField

from tasks.models import TaskFile


class TaskFileSerializer(ModelSerializer):
    """
    Сериализатор файлов задачи
    """

    file = FileField()

    class Meta:
        model = TaskFile
        fields = ("file",)
