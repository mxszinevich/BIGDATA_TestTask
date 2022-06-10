from rest_framework.routers import DefaultRouter

from users.viewset import UserViewSet

router = DefaultRouter()

# users
router.register("users", UserViewSet, basename="users")
