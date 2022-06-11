import pytest
from django.urls import reverse
from rest_framework import status

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

    @pytest.mark.django_db
    def test_jwt_token_authorization(self, api_client):
        """
        Тестирование авторизации с помощью jwt токена
        """

        url = reverse("jwt-create")
        user = UserFactory()
        data = {"username": user.username, "password": USER_FAKE_PASSWORD}
        response = api_client.post(url, data=data)
        assert response.status_code == 200
        res_json = response.json()
        access_token = res_json["access"]

        url = reverse("users-detail", kwargs={"id": user.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        api_client.credentials(HTTP_AUTHORIZATION=f"JWT {access_token}")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
