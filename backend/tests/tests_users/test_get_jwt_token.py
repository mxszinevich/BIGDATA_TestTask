import pytest
from django.urls import reverse
from tests.tests_users.user_factory import UserFactory, USER_FAKE_PASSWORD


class TestGetJwtToken:
    """
    Тестирование API пользователей
    """

    @pytest.mark.django_db
    def test_get_jwt_token(self, api_client):
        """
        Тестирование получение jwt-токена
        """

        url = reverse("jwt-create")
        user = UserFactory()
        data = {"username": user.username, "password": USER_FAKE_PASSWORD}
        response = api_client.post(url, data=data)
        assert response.status_code == 200
        res_json = response.json()
        assert "refresh" in res_json
        assert "access" in res_json

        data = {"username": user.username, "password": "12313sdfc"}
        response = api_client.post(url, data=data)
        assert response.status_code == 401
