from django.contrib import admin

from tasks.admin import TaskFileInline
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Задачи
    """

    inlines = [TaskFileInline]
