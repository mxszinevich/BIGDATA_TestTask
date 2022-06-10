from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(tags=["Users"])
class UserViewSet(UserViewSet):
    """
    Пользователи
    """

    http_method_names = ["get", "post"]

    activation = None
    resend_activation = None
    reset_username_confirm = None
    reset_password = None
    reset_password_confirm = None
    reset_username = None
    set_username = None
    set_password = None
    me = None

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="first_name",
                description="Имя пользователя",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="last_name",
                description="Фамилия пользователя",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="patronymic",
                description="Отчество пользователя",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="username",
                description="Логин пользователя",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="password",
                description="Пароль пользователя",
                required=True,
                type=str,
            ),
        ],
        description="Регистрация пользователя",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
