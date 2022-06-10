# from djoser.urls.jwt import
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenCreateViewSet(TokenObtainPairView):
    """
    Создание токена
    """
