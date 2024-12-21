from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from backend.views import hello_world

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Test endpoint
    path("api/hello-world/", hello_world),
    # Core App API
    path("api/", include("core.urls")),
    # Silk
    path("silk/", include("silk.urls", namespace="silk")),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
