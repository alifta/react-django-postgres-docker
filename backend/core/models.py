import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model"""

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Product(models.Model):
    """Represents a product in the system"""

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    @property
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):
    """Represents an order in the system"""

    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"
        DELIVERED = "Delivered"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )

    def __str__(self):
        return f"Order {self.order_id } by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"


class Recipe(models.Model):
    """Represents a recipe in the system"""

    name = models.CharField(max_length=255)
    description = models.TextField()
    # ingredients = models.TextField()
    # directions = models.TextField()
    # image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.name
