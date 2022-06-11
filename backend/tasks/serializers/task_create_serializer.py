from rest_framework.serializers import ModelSerializer

from tasks.models import Task
from tasks.serializers import TaskFileSerializer


class TaskCreateSerializer(ModelSerializer):
    """
    Сериализатор создания задачи
    """

    files = TaskFileSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = "__all__"
