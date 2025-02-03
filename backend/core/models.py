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

# Models tha we can add later:
# - Media (Images, Videos, etc.) for users, peroperties or projects
#     - updated_by, created_by, created_at, updated_at, media_category, media_group, media_type, media_name, media_description, media_url, media_status, media_tags
# - Projects (Projects, Tasks, etc.)
#     - project_id, project_name, project_description, project_status, project_start_date, project_end_date, project_budget, project_currency, project_manager, project_team, project_client, project_location, project_tags
# - Tasks (Tasks, Subtasks, etc.)
#     - task_id, task_name, task_description, task_status, task_start_date, task_end_date, task_priority, task_assignee, task_tags
# - Comments (Comments, Reviews, etc.)
#     - comment_id, comment_text, comment_status, comment_created_at, comment_updated_at, comment_created_by, comment_updated_by, comment_tags
# - Notifications (Notifications, Alerts, etc.)
#     - notification_id, notification_text, notification_status, notification_created_at, notification_updated_at, notification_created_by, notification_updated_by, notification_tags
# - Messages (Messages, Emails, etc.)
#     - message_id, message_subject, message_text, message_status, message_created_at, message_updated_at, message_created_by, message_updated_by, message_tags
# - Bookings (Bookings, Reservations, etc.)
#     - booking_id, booking_start_date, booking_end_date, booking_status, booking_created_at, booking_updated_at, booking_created_by, booking_updated_by, booking_tags
# - Payments (Payments, Invoices, etc.)
#     - payment_id, payment_amount, payment_method, payment_status, payment_created_at, payment_updated_at, payment_created_by, payment_updated_by, payment_tags
# - Reviews (Reviews, Ratings, etc.)
#     - review_id, review_rating, review_text, review_status, review_created_at, review_updated_at, review_created_by, review_updated_by, review_tags
# - Favorites (Favorites, Likes, etc.)
#     - favorite_id, favorite_status, favorite_created_at, favorite_updated_at, favorite_created_by, favorite_updated_by, favorite_tags


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "recipe", filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user."""
        if not email:
            raise ValueError("The Email field must be set.")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# LANGUAGE
class Language(models.Model):
    """Language model."""

    language_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, help_text="Language name")

    class Meta:
        db_table = "languages"

    def __str__(self):
        return self.name


# ADDRESS
class Address(models.Model):
    """Address model."""

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.country}"


# TAG
class Tag(models.Model):
    """A generic Tag model for tagging objects"""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name


# USER
class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    class UserStatuses(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        PENDING = "pending", "Pending"
        SUSPENDED = "suspended", "Suspended"
        DELETED = "deleted", "Deleted"

    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    roles = models.ManyToManyField(
        "Role",
        through="UserRole",
        related_name="users",
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatuses.choices,
        default=UserStatuses.ACTIVE,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


# An abstract base model to add created/updated info
class BaseActivity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # These use SET_NULL so that if a user is removed, the activity remains.
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )


# ROLE
class Role(models.Model):
    """User roles model."""

    class RoleTypes(models.TextChoices):
        ADMIN = "admin", "Admin"
        GUEST = "guest", "Guest"
        PARTNER = "partner", "Partner"
        HOMEOWNER = "homeowner", "Homeowner"
        DESIGNER = "designer", "Designer"
        ARCHITECT = "architect", "Architect"
        DEVELOPER = "developer", "Developer"
        CONTRACTOR = "contractor", "Contractor"
        ENGINEER = "engineer", "Engineer"
        SUPPLIER = "supplier", "Supplier"
        VENDOR = "vendor", "Vendor"
        AGENT = "agent", "Agent"
        BROKER = "broker", "Broker"
        INSPECTOR = "inspector", "Inspector"
        APPRAISER = "appraiser", "Appraiser"
        INVESTOR = "investor", "Investor"
        LENDER = "lender", "Lender"
        TENANT = "tenant", "Tenant"
        ADVISOR = "advisor", "Advisor"

    role_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(
        max_length=20, choices=RoleTypes.choices, default=RoleTypes.HOMEOWNER
    )

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


# ORGANIZATION
class Organization(models.Model):
    """Organization model."""

    organization_id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=255, unique=True, help_text="The name of the organization or firm."
    )
    description = models.TextField(
        blank=True, null=True, help_text="A short description of the organization."
    )
    # If you want to reuse your existing Address model:
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="organizations",
        help_text="Physical address of the organization.",
    )
    website = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The organization's website URL.",
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Contact phone number for the organization.",
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        help_text="Contact email address for the organization.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


# PROFILE
class Profile(models.Model):
    """User profile model."""

    profile_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="profiles",
    )
    role = models.OneToOneField(Role, on_delete=models.CASCADE, db_column="role_id")
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="members",
        help_text="The organization this user (profile) is affiliated with.",
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_phone = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    languages = models.ManyToManyField(
        Language,
        through="ProfileLanguage",
        related_name="profiles",
    )
    bio = models.TextField(blank=True, null=True)
    cv = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        db_column="address_id",
        blank=True,
        null=True,
        related_name="profiles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return f"{self.full_name}"


# PROFILE LANGUAGE
class ProfileLanguage(models.Model):
    """Profile language model captures many-to-many relationship between user profiles and languages."""

    class ProficiencyLevels(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        FLUENT = "fluent", "Fluent"
        NATIVE = "native", "Native"

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_column="profile_id",
        related_name="profile_languages",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        db_column="language_id",
        related_name="language_profiles",
    )
    proficiency = models.CharField(
        max_length=20,
        choices=ProficiencyLevels.choices,
        default=ProficiencyLevels.FLUENT,
        help_text="Language proficiency level",
    )

    class Meta:
        db_table = "profile_languages"

    def __str__(self):
        return f"{self.profile.full_name} -> {self.language.name}"


# USER ROLE
class UserRole(models.Model):
    """User role link model captures many-to-many relationship between users and roles."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        db_column="role_id",
        related_name="role_users",
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="assigner_user_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_roles"

    def __str__(self):
        return f"{self.user.email} -> {self.role.name}"


# APPLIANCE
class Appliance(models.Model):
    """Appliance model."""

    class ApplianceTypes(models.TextChoices):
        KITCHEN = "kitchen", "Kitchen"
        LAUNDRY = "laundry", "Laundry"
        HVAC = "hvac", "HVAC"
        WATER_HEATER = "water_heater", "Water Heater"
        OTHER = "other", "Other"

    name = models.CharField(
        max_length=255,
        help_text="Name of the appliance.",
    )
    description = models.TextField(
        blank=True,
        help_text="A brief description of the appliance.",
    )
    brand = models.CharField(
        max_length=255,
        blank=True,
        help_text="The manufacturer or brand of the appliance.",
    )
    model = models.CharField(
        max_length=255,
        blank=True,
        help_text="The model designation or number.",
    )
    serial_number = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
        help_text="The serial number of the appliance.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "appliances"
        ordering = ["name"]
        verbose_name = "Appliance"
        verbose_name_plural = "Appliances"

    def __str__(self):
        return self.name


# PROPERTY
class Property(models.Model):
    """Property model representing a real estate property."""

    class PropertyTypes(models.TextChoices):
        HOUSE = "house", "House"
        APARTMENT = "apartment", "Apartment"
        CONDO = "condo", "Condo"
        TOWNHOUSE = "townhouse", "Townhouse"

    property_id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the property listing.",
    )
    description = models.TextField(
        help_text="Detailed description of the property.",
    )
    property_type = models.CharField(
        max_length=15,
        choices=PropertyTypes.choices,
        default=PropertyTypes.HOUSE,
        help_text="Type of property (e.g., House, Apartment, etc.).",
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        db_column="address_id",
        null=True,
        blank=True,
        related_name="property",
        help_text="Address of the property.",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_column="user_id",
        related_name="properties",
        help_text="Owner of the property.",
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Current price of the property as determined by the seller or agent.",
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Indicates if the property is currently available on the market.",
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Indicates if the property is published or still in draft.",
    )
    lot_area = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total area of the lot in square meters",
    )
    floor_area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Total livable area within the structure in square meters.",
    )
    ceiling_height = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Height of the ceiling in meters.",
    )
    num_floors = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total number of floors (stories) in the property",
    )
    num_rooms = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total number of rooms in the property.",
    )
    num_bathrooms = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total number of bathrooms in the property.",
    )
    num_parking = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total number of parking spaces available with the property.",
    )
    open_parking = models.BooleanField(
        default=False,
        help_text="Indicates if open (uncovered) parking spaces are available.",
    )
    covered_parking = models.BooleanField(
        default=False,
        help_text="Indicates if covered (garage) parking spaces are available.",
    )
    year_built = models.DateField(
        blank=True,
        null=True,
        help_text="The date when the property was built.",
    )
    tax_assessed_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Property value as per the latest tax assessment.",
    )
    tax_annual_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Annual property tax amount.",
    )
    appliances = models.ManyToManyField(
        Appliance,
        related_name="properties",
        blank=True,
        help_text="List of appliances included with the property.",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or remarks regarding the property.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def lot_area_square_feet(self) -> float:
        """Convert lot area from square meters to square feet.

        Returns 0.0 if lot_area is not provided.
        """
        if self.lot_area:
            return self.lot_area * 10.76391041671
        return 0.0

    class Meta:
        db_table = "properties"
        ordering = ["-created_at"]
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title


# PROPERTY PHOTO
class PropertyPhoto(models.Model):
    """Property photo model."""

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
    """Amenity model."""

    amenity_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "amenities"

    def __str__(self):
        return self.name


# PROPERTY AMENITY
class PropertyAmenity(models.Model):
    """Property amenity model captures many-to-many relationship between properties and amenities."""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        db_column="property_id",
        related_name="property_amenities",
    )
    amenity = models.ForeignKey(
        Amenity,
        on_delete=models.CASCADE,
        db_column="amenity_id",
        related_name="amenity_properties",
    )

    class Meta:
        db_table = "property_amenities"
        constraints = [
            models.UniqueConstraint(
                fields=["property", "amenity"], name="unique_property_amenity"
            )
        ]

    def __str__(self):
        return f"{self.property.title} -> {self.amenity.name}"


# OPENHOUSE
class OpenHouse(models.Model):
    """Open house model."""

    METHOD_CHOICES = (
        ("virtual", "Virtual"),
        ("in-person", "In-Person"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("cancelled", "Cancelled"),
        ("ended", "Ended"),
        ("deleted", "Deleted"),
    )

    openhouse_id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, db_column="property_id"
    )
    agents = models.ManyToManyField(User, through="OpenHouseAgent")
    date = models.DateTimeField(null=True, blank=True)
    starttime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default="in-person",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    notes = models.TextField(null=True, blank=True)
    attendess = models.TextField(null=True, blank=True)
    virtual_url = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "openhouses"

    def __str__(self):
        return f"OpenHouse {self.property.title} - {self.date}"


# OPENHOUSE AGENT
class OpenHouseAgent(models.Model):
    """Open house agent model captures many-to-many relationship between openhouses and agent users."""

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
        ("deleted", "Deleted"),
    )

    openhouse = models.ForeignKey(
        OpenHouse,
        on_delete=models.CASCADE,
        db_column="openhouse_id",
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="agent_id",
        related_name="agent_openhouses",
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    class Meta:
        db_table = "openhouse_agents"

    def __str__(self):
        return f"{self.openhouse.openhouse_id} - {self.status}"


# BOOKING
class Booking(models.Model):
    """Booking model."""

    booking_id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        db_column="property_id",
    )
    guest = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    check_in = models.DateField(blank=True, null=True)
    check_out = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookings"

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property.title}"


# PAYMENT
class Payment(models.Model):
    """Payment model."""

    payment_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        db_column="booking_id",
    )
    # transaction = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking_id}"


# REVIEW
class Review(models.Model):
    """Review model."""

    review_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, db_column="booking_id"
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


# FAVORITE
class Favorite(models.Model):
    """Favorite model."""

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


# MESSAGE
class Message(models.Model):
    """Message model."""

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


# NOTIFICATION
class Notification(models.Model):
    """Notification model."""

    notification_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f"Notification {self.notification_id} for {self.user.email}"


# PRODUCT
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


# ORDER
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
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product,
        through="OrderItem",
        related_name="orders",
    )

    def __str__(self):
        return f"Order {self.order_id} by {self.user.email}"


# ORDER ITEM
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"


# RECIPE
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


# TAG
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
