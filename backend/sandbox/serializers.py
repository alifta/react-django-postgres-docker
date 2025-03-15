from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for Restaurant objects."""

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "website",
            "date_opened",
            "latitude",
            "longitude",
        )
        read_only_fields = ("id",)
