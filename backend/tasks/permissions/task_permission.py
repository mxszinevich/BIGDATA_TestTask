from rest_framework.permissions import BasePermission


class TaskPermission(BasePermission):
    """
    Разграничение прав API задач
    """

    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.user == request.user
