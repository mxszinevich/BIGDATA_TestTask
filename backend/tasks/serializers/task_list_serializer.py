from rest_framework.serializers import ModelSerializer

from tasks.models import Task
from tasks.serializers import TaskFileSerializer


class TaskListSerializer(ModelSerializer):
    """
    Сериализатор списка задач
    """

    class Meta:
        model = Task
        fields = "__all__"
