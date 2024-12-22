from django.db.models import Max
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from core.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from core.models import Product, Order, OrderItem
from core.filters import ProductFilter, InStockFilterBackend


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "stock", "created_at"]
    # Override the default pagination settings
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.max_page_size = 10
    pagination_class.page_size_query_param = "size"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"  # pk is default

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items", "items__product").all()
#     serializer_class = OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items", "items__product").all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_permissions(self):
    #     self.permission_classes = [IsAuthenticated]
    #     if self.action == "create":
    #         self.permission_classes = [IsAuthenticated]
    #     return super().get_permissions()


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items", "items__product").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)
