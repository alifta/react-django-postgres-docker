"""
Database models.
"""

import os
import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "recipe", filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create and return a new superuser."""
        # extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# USER
# class User(AbstractUser, PermissionsMixin):
class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    # user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(
        max_length=255, blank=True
    )  # TODO: Deprecate this field and move it to UserProfile or change it to user_name
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # cv = models.FileField(upload_to="cvs/", blank=True, null=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


# USER_PROFILE
class UserProfile(models.Model):
    """User profile model."""

    profile_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# USER_ROLE
class UserRole(models.Model):
    """User roles model."""

    role_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "user_roles"

    def __str__(self):
        return self.name


# 4. USER_ROLE_LINK
class UserRoleLink(models.Model):
    """User role link model captures relationsheep between users and roles."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, db_column="role_id")

    class Meta:
        db_table = "user_role_link"
        unique_together = (("user", "role"),)

    def __str__(self):
        return f"{self.user.email} -> {self.role.name}"


# PROPERTY
class Property(models.Model):
    property_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=10, decimal_places=7, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7, blank=True, null=True
    )
    price = models.DecimalField(max_digits=100, decimal_places=2)
    is_available = models.BooleanField(default=True)
    floor_area = models.FloatField(blank=True, null=True)
    ceiling_height = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )
    num_rooms = models.PositiveIntegerField(blank=True, null=True)
    flooring_material = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "properties"

    def __str__(self):
        return self.title


# PROPERTY_PHOTO
class PropertyPhoto(models.Model):
    photo_id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, db_column="property_id"
    )
    photo_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "property_photos"

    def __str__(self):
        return f"{self.property.title} -> Photo {self.photo_id}"


# AMENITIES
class Amenity(models.Model):
    amenity_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "amenities"

    def __str__(self):
        return self.name


# PROPERTY_AMENITY_LINK
class PropertyAmenityLink(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, db_column="property_id"
    )
    amenity = models.ForeignKey(
        Amenity, on_delete=models.CASCADE, db_column="amenity_id"
    )

    class Meta:
        db_table = "property_amenity_link"
        unique_together = (("property", "amenity"),)

    def __str__(self):
        return f"{self.property.title} -> {self.amenity.name}"


# OPEN HOUSE
class OpenHouse(models.Model):
    # Primary Key
    open_house_id = models.BigAutoField(primary_key=True)

    # Identifiers
    open_house_key = models.CharField(
        max_length=50, unique=True, db_column="OpenHouseKey"
    )
    open_house_key_numeric = models.BigIntegerField(
        null=True, blank=True, db_column="OpenHouseKeyNumeric"
    )
    open_house_id_value = models.CharField(
        max_length=50, null=True, blank=True, db_column="OpenHouseId"
    )
    listing_id = models.CharField(
        max_length=50, null=True, blank=True, db_column="ListingId"
    )
    listing_key = models.CharField(
        max_length=50, null=True, blank=True, db_column="ListingKey"
    )
    listing_key_numeric = models.BigIntegerField(
        null=True, blank=True, db_column="ListingKeyNumeric"
    )

    # Timestamps
    modification_timestamp = models.DateTimeField(
        null=True, blank=True, db_column="ModificationTimestamp"
    )
    original_entry_timestamp = models.DateTimeField(
        null=True, blank=True, db_column="OriginalEntryTimestamp"
    )
    bridge_modification_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        db_column="BridgeModificationTimestamp",
        help_text="Timestamp last modified in the Bridge system (if applicable).",
    )

    # Open House Info
    open_house_date = models.DateTimeField(
        null=True, blank=True, db_column="OpenHouseDate"
    )
    open_house_start_time = models.DateTimeField(
        null=True, blank=True, db_column="OpenHouseStartTime"
    )
    open_house_end_time = models.DateTimeField(
        null=True, blank=True, db_column="OpenHouseEndTime"
    )
    open_house_remarks = models.TextField(
        null=True, blank=True, db_column="OpenHouseRemarks"
    )
    open_house_attended_by = models.CharField(
        max_length=100, null=True, blank=True, db_column="OpenHouseAttendedBy"
    )
    open_house_method = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column="OpenHouseMethod",
        help_text="In-person or virtual, etc.",
    )
    appointment_required_yn = models.BooleanField(
        null=True, blank=True, db_column="AppointmentRequiredYN"
    )
    refreshments = models.TextField(null=True, blank=True, db_column="Refreshments")

    # If your open_house_status is single-valued:
    open_house_status = models.CharField(
        max_length=50, null=True, blank=True, db_column="OpenHouseStatus"
    )
    # If `Status` can be multi-valued in the JSON, you might store it
    # in a separate model (OpenHouseStatus) instead.

    # Additional Virtual Info
    virtual_open_house_url = models.CharField(
        max_length=255, null=True, blank=True, db_column="VirtualOpenHouseURL"
    )
    livestream_open_house_url = models.CharField(
        max_length=255, null=True, blank=True, db_column="LivestreamOpenHouseURL"
    )

    # Agent Info
    showing_agent_first_name = models.CharField(
        max_length=100, null=True, blank=True, db_column="ShowingAgentFirstName"
    )
    showing_agent_last_name = models.CharField(
        max_length=100, null=True, blank=True, db_column="ShowingAgentLastName"
    )
    showing_agent_key = models.CharField(
        max_length=50, null=True, blank=True, db_column="ShowingAgentKey"
    )
    showing_agent_key_numeric = models.BigIntegerField(
        null=True, blank=True, db_column="ShowingAgentKeyNumeric"
    )
    showing_agent_mls_id = models.CharField(
        max_length=50, null=True, blank=True, db_column="ShowingAgentMlsID"
    )

    # Systems
    originating_system_id = models.CharField(
        max_length=50, null=True, blank=True, db_column="OriginatingSystemID"
    )
    originating_system_key = models.CharField(
        max_length=50, null=True, blank=True, db_column="OriginatingSystemKey"
    )
    originating_system_name = models.CharField(
        max_length=100, null=True, blank=True, db_column="OriginatingSystemName"
    )
    source_system_id = models.CharField(
        max_length=50, null=True, blank=True, db_column="SourceSystemID"
    )
    source_system_key = models.CharField(
        max_length=50, null=True, blank=True, db_column="SourceSystemKey"
    )
    source_system_name = models.CharField(
        max_length=100, null=True, blank=True, db_column="SourceSystemName"
    )

    # Potential "Attended" from JSON
    attended = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column="Attended",
        help_text="Could be 'Attended by agent', 'Unattended', 'Attended by seller', etc.",
    )

    class Meta:
        db_table = "open_house"

    def __str__(self):
        return f"OpenHouse {self.open_house_key} - {self.open_house_date}"


class OpenHouseType(models.Model):
    """
    If OpenHouseType is an array, we store each type as a row here.
    E.g. "Public", "Broker", "Office", etc.
    """

    id = models.BigAutoField(primary_key=True)
    open_house = models.ForeignKey(
        OpenHouse,
        on_delete=models.CASCADE,
        db_column="open_house_id",
        related_name="house_types",
    )
    type_value = models.CharField(max_length=50, db_column="OpenHouseType")

    class Meta:
        db_table = "open_house_types"

    def __str__(self):
        return f"{self.open_house.open_house_key} - {self.type_value}"


class OpenHouseStatus(models.Model):
    """
    If 'Status' can be multiple in the JSON, store them here.
    E.g. "Active", "Cancelled", "Ended", etc.
    """

    id = models.BigAutoField(primary_key=True)
    open_house = models.ForeignKey(
        OpenHouse,
        on_delete=models.CASCADE,
        db_column="open_house_id",
        related_name="house_statuses",
    )
    status_value = models.CharField(max_length=50, db_column="OpenHouseStatus")

    class Meta:
        db_table = "open_house_statuses"

    def __str__(self):
        return f"{self.open_house.open_house_key} - {self.status_value}"


# 9. BOOKINGS
class Bookings(models.Model):
    booking_id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, db_column="property_id"
    )
    guest = models.ForeignKey(User, on_delete=models.CASCADE, db_column="guest_id")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookings"

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property.title}"


# 10. PAYMENTS
class Payments(models.Model):
    payment_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(
        Bookings, on_delete=models.CASCADE, db_column="booking_id"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default="pending")
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking_id}"


# 11. REVIEWS
class Reviews(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(
        Bookings, on_delete=models.CASCADE, db_column="booking_id"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="reviewer_id"
    )
    rating = models.SmallIntegerField()  # Or models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"Review {self.review_id} - Rating: {self.rating}"


# 12. FAVORITES
class Favorites(models.Model):
    favorite_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, db_column="property_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorites"

    def __str__(self):
        return f"Favorite {self.favorite_id} by {self.user.email}"


# 13. MESSAGES
class Messages(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        db_column="sender_id",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
        db_column="receiver_id",
    )
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email} to {self.receiver.email}"


# 14. NOTIFICATIONS
class Notifications(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f"Notification {self.notification_id} for {self.user.email}"


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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )

    def __str__(self):
        return f"Order {self.order_id } by {self.user.email}"


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
    """Recipe object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.URLField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for filtering recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
