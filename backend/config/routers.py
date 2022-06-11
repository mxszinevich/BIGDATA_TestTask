from rest_framework.routers import DefaultRouter

from tasks.viewset import TaskViewSet
from users.viewset import UserViewSet

router = DefaultRouter()

# users
router.register("users", UserViewSet, basename="users")

# tasks
router.register("tasks", TaskViewSet, basename="tasks")
