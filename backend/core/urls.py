from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view()),
    path("products/info/", views.ProductInfoAPIView.as_view()),
    path(
        "products/<int:product_id>/",
        views.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    path(
        "location/",
        views.LocationListCreateAPIView.as_view(),
        name="location",
    ),
    path(
        "location/<int:location_id>/",
        views.LocationDetailAPIView.as_view(),
        name="location-detail",
    ),
    # HTMX views
    path("contacts/", views.index, name="index"),
    path("contacts-search/", views.search_contacts, name="contacts-search"),
]

router = DefaultRouter()
router.register("orders", views.OrderViewSet)
urlpatterns += router.urls
