from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from config.routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls.jwt")),
    path("api/", include(router.urls)),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
