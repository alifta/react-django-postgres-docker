from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Lower


def validate_restaurant_name_begins_with_a(value):
    if not value.startswith("a"):
        raise ValidationError("Restaurant name must start with 'a'.")
    return value


class Contact(models.Model):
    """Contact model."""

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contacts"
        unique_together = ("user", "email")

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Restaurant(models.Model):
    """Restaurant model."""

    class TypeChoices(models.TextChoices):
        INDIAN = "IN", "Indian"
        CHINESE = "CH", "Chinese"
        ITALIAN = "IT", "Italian"
        GREEK = "GR", "Greek"
        MEXICAN = "MX", "Mexican"
        FASTFOOD = "FF", "Fast Food"
        OTHER = "OT", "Other"

    name = models.CharField(
        max_length=100, validators=[validate_restaurant_name_begins_with_a]
    )
    website = models.URLField(max_length=255, blank=True, null=True)
    date_opened = models.DateField(blank=True, null=True)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    restaurant_type = models.CharField(
        max_length=2,
        choices=TypeChoices.choices,
        default=TypeChoices.OTHER,
    )

    class Meta:
        db_table = "restaurants"
        ordering = [Lower("name"), "date_opened"]
        get_latest_by = "date_opened"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the restaurant is being created for the first time
        print(self._state.adding)
        super().save(*args, **kwargs)


class Rating(models.Model):
    """Rating model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        db_table = "ratings"

    def __str__(self):
        return f"Rating: {self.rating}"


class Sale(models.Model):
    """Sale model."""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sales",
    )
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()

    class Meta:
        db_table = "sales"

    def __str__(self):
        return f"Sale: {self.income}"
