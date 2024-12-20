from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from core.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from core.models import Product, Order, OrderItem


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    # queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"  # pk is default


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items", "items__product").all()
    serializer_class = OrderSerializer


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
