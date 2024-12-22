from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view()),
    path("products/info/", views.ProductInfoAPIView.as_view()),
    path("products/<int:product_id>/", views.ProductDetailAPIView.as_view()),
    # path("orders/", views.OrderListAPIView.as_view()),
    # path("user-orders/", views.UserOrderListAPIView.as_view(), name="user-orders"),
]

router = DefaultRouter()
# router.register(r"orders", views.OrderViewSet)
router.register("orders", views.OrderViewSet)
urlpatterns += router.urls
