from rest_framework import generics

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    """View for listing and creating restaurants."""

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a restaurant."""

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
