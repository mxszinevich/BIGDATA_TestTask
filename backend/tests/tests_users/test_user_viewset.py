import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User


class TestUserViewSet:
    """
    Тестирование API пользователей
    """

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "username, password, first_name, last_name, patronymic, status_code",
        [
            ("username", "123456#QAZ", "user", "user", "user", status.HTTP_201_CREATED),
            ("", "123456#QAZ", "user", "user", "user", status.HTTP_400_BAD_REQUEST),
            ("username", "", "user", "user", "user", status.HTTP_400_BAD_REQUEST),
            ("username", "123456#QAZ", "", "user", "user", status.HTTP_400_BAD_REQUEST),
            ("username", "123456#QAZ", "user", "", "user", status.HTTP_400_BAD_REQUEST),
            ("username", "123456#QAZ", "user", "user", "", status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_registrations_user(
        self,
        api_client,
        django_assert_num_queries,
        username,
        password,
        first_name,
        last_name,
        patronymic,
        status_code,
    ):
        """
        Тестирование регистрации пользователей
        """
        url = reverse("users-list")
        user_data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "patronymic": patronymic,
        }
        response = api_client.post(url, data=user_data)
        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            assert User.objects.count() == 1
            user = User.objects.first()
            assert user.username == "username"
            assert user.last_name == "user"
