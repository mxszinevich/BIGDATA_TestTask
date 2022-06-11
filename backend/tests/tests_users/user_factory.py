from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory

from users.models import User

USER_FAKE_PASSWORD = "password"


class UserFactory(DjangoModelFactory):
    """
    Фабрика модели пользователя
    """

    username = Faker("name")
    first_name = Faker("name")
    last_name = Faker("name")
    patronymic = Faker("name")
    password = PostGenerationMethodCall("set_password", USER_FAKE_PASSWORD)
    is_active = True

    class Meta:
        model = User
