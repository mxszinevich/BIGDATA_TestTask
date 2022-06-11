from rest_framework.serializers import ModelSerializer, CharField

from tasks.models import Task
from tasks.serializers import TaskFileSerializer
from tasks.validators import validate_completion_date


class TaskCreateSerializer(ModelSerializer):
    """
    Сериализатор создания задачи
    """

    files = TaskFileSerializer(many=True, required=False)
    completion_date = CharField(required=True, validators=[validate_completion_date])

    class Meta:
        model = Task
        fields = "__all__"
