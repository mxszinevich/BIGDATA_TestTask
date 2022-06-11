from rest_framework.serializers import ModelSerializer, CharField

from tasks.models import Task
from tasks.serializers import TaskFileSerializer
from tasks.validators import validate_completion_date


class TaskUpdateSerializer(ModelSerializer):
    """
    Сериализатор обновления задачи
    """

    title = CharField(required=False)
    description = CharField(required=False)
    completion_date = CharField(required=False, validators=[validate_completion_date])
    files = TaskFileSerializer(many=True, required=False)

    class Meta:
        model = Task
        exclude = ("id", "user")
