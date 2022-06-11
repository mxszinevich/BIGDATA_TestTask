from rest_framework.serializers import CharField
from djoser.serializers import UserCreateSerializer


class UserRegistrationSerializer(UserCreateSerializer):
    """
    Регистрация пользователя
    """

    first_name = CharField(required=True)
    last_name = CharField(required=True)
    patronymic = CharField(required=True)
