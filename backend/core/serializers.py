from django.db import transaction
from rest_framework import serializers

from .models import Location, Order, OrderItem, Product, TaggedItem, User


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location objects."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Location
        fields = (
            "location_id",
            # "address",
            "latitude",
            "longitude",
            "user",
            # "tags",
        )
        read_only_fields = ("location_id",)

    def validate_latitude(self, value):
        """Validate the latitude value."""
        if not (-90 <= value <= 90):
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value):
        """Validate the longitude value."""
        if not (-180 <= value <= 180):
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        location = Location.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = TaggedItem.objects.get_or_create(**tag_data)
            location.tags.add(tag)
        return location

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = TaggedItem.objects.get_or_create(**tag_data)
                instance.tags.add(tag)
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        # fields = "__all__"
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price"
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal",
        )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an order."""

    class OrderItemCreateSerializer(serializers.ModelSerializer):
        """Serializer for creating an order item inside an order API request."""

        class Meta:
            model = OrderItem
            fields = ("product", "quantity")

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("items")

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if order_items_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all().delete()

                # Recreate items with updated dataß
                for item in order_items_data:
                    OrderItem.objects.create(order=instance, **item)

        return instance

    def create(self, validated_data):
        order_items_data = validated_data.pop("items")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in order_items_data:
                OrderItem.objects.create(order=order, **item)

        return order

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            "items",
        )
        extra_kwargs = {
            "user": {"read_only": True},
        }


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    # items = OrderItemSerializer(many=True, read_only=True)
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            "created_at",
            "items",
            "total_price",
        )


class ProductInfoSerializer(serializers.Serializer):
    # Get all products, count of products, and, max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
