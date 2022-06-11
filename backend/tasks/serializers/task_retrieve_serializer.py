from rest_framework.serializers import ModelSerializer

from tasks.models import Task
from tasks.serializers import TaskFileSerializer


class TaskRetrieveSerializer(ModelSerializer):
    """
    Сериализатор детальной информации о задаче
    """

    files = TaskFileSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
