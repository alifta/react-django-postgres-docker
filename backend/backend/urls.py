from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core import views as core_views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health check
    path("api/health-check/", core_views.health_check, name="health-check"),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # Core
    path("api/", include("core.urls")),
    # User
    path("api/user/", include("user.urls")),
    # Recipe
    path("api/recipe/", include("recipe.urls")),
    # Silk - must be the last URL
    path("silk/", include("silk.urls", namespace="silk")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
