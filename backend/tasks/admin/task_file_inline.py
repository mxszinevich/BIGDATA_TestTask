from django.contrib import admin

from tasks.models import TaskFile


class TaskFileInline(admin.TabularInline):
    """
    Файл задачи
    """

    model = TaskFile
    extra = 0
