from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter

from tasks.models import Task
from tasks.permissions import TaskPermission
from tasks.serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskFileSerializer,
    TaskRetrieveSerializer,
    TaskUpdateSerializer,
)


@extend_schema(tags=["Tasks"])
class TaskViewSet(ModelViewSet):
    """
    Задачи.
    Необходима авторизация: Authorization: JWT access_token
    """

    permission_classes = [TaskPermission]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        serializer_class = TaskListSerializer
        if self.action == self.create.__name__:
            serializer_class = TaskCreateSerializer
        if self.action == self.update.__name__:
            serializer_class = TaskUpdateSerializer
        elif self.action == self.retrieve.__name__:
            serializer_class = TaskRetrieveSerializer

        return serializer_class

    def get_queryset(self):
        queryset = (
            Task.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("files")
        )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                description="Название задачи",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="description",
                description="Описание задачи",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="completion_date",
                description="Дата завершения задачи. Формат: YYYY-MM-DD",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="user",
                description="ID пользователя",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="files",
                description="Файлы задачи",
                type=TaskFileSerializer,
            ),
        ],
        description="Создание задачи. Для создания необходима авторизация: Authorization: JWT access_token",
    )
    @parser_classes([MultiPartParser])
    def create(self, request, *args, **kwargs):
        """
        Создание задачи с учетом передачи нескольких файлов
        """

        task_serializer = self.get_serializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        task: Task = task_serializer.save(user=request.user)

        for file in request.data.getlist("files"):
            files_serializer = TaskFileSerializer(data={"file": file})
            files_serializer.is_valid(raise_exception=True)
            files_serializer.save(task=task)

        return Response(task_serializer.data, status=status.HTTP_201_CREATED)
