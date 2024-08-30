from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .views import ping


base_prefix = "api/v1"

urlpatterns = [
    # auth endpoints
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    # Base endpoints
    path("ping/", ping, name="ping"),
    path("admin/", admin.site.urls),
    # Schemas
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Apps endpoints
    path(f"{base_prefix}/parcel/", include("parcel.urls")),
    path(f"{base_prefix}/weather/", include("weather.urls")),
]
