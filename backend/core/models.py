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
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

# =======
# Utility
# =======


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "recipe", filename)


# ======
# Models
# ======


class Activity(models.Model):
    """
    An abstract activity model for adding created_*/updated_* fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created.",
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated.",
        verbose_name="Updated At",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
        help_text="User who created this record.",
        verbose_name="Created By",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
        help_text="User who last updated this record.",
        verbose_name="Updated By",
    )

    def save(self, *args, **kwargs):
        """
        Set created_by and updated_by if a 'user' keyword argument is provided.
        """

        user = kwargs.pop("user", None)
        if user:
            if not self.pk and not self.created_by:
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["created_by"]),
            models.Index(fields=["updated_by"]),
        ]


class Timestamp(models.Model):
    """
    An abstract timestamp model that adds created and updated timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when this record was created.",
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when this record was last updated.",
        verbose_name="Updated At",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        verbose_name = "Timestamp"
        verbose_name_plural = "Timestamps"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]


# class Tag(models.Model):
#     """Tag model."""

#     tag_name = models.CharField(
#         max_length=100,
#         help_text="Name for the tag.",
#         verbose_name="Tag Name",
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         db_column="user_id",
#         related_name="created_tags",
#         help_text="User who created this tag.",
#         verbose_name="Created By",
#     )

#     class Meta:
#         db_table = "tags"
#         ordering = ["tag_name"]
#         verbose_name = "Tag"
#         verbose_name_plural = "Tags"
#         indexes = [
#             models.Index(fields=["tag_name"]),
#         ]


class TaggedItem(models.Model):
    """Through model for managing many-to-many relationships with tags."""

    # tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="created_tags",
        help_text="User who created this tag.",
        verbose_name="Created By",
    )

    class Meta:
        db_table = "tags"
        unique_together = ("tag", "user", "content_type", "object_id")
        indexes = [
            models.Index(fields=["tag"]),
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.tag} for user {self.user}"


class UserManager(BaseUserManager):
    """Manager for user model."""

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


class User(AbstractBaseUser, PermissionsMixin, Activity):
    """
    User Model.
    """

    class UserStatuses(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        PENDING = "pending", "Pending"
        SUSPENDED = "suspended", "Suspended"
        DELETED = "deleted", "Deleted"

    # Primary key field
    user_id = models.BigAutoField(primary_key=True)
    # user_id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False,
    #     unique=True,
    # )
    # Email is the unique identifier for authentication
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        help_text="User email address, used as the username for login.",
        verbose_name="Email Address",
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="First name of the user.",
        verbose_name="First Name",
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Last name of the user.",
        verbose_name="Last Name",
    )
    # Many-to-many relationship to tags through the TaggedItem table
    tags = GenericRelation(
        TaggedItem,
        related_query_name="users",
    )
    # Many-to-many relationship to roles through the UsersRoles table
    roles = models.ManyToManyField(
        "Role",
        through="UserRole",
        through_fields=("user", "role"),
        related_name="users",
        help_text="Roles assigned to the user.",
        verbose_name="Assigned Roles",
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatuses.choices,
        default=UserStatuses.ACTIVE,
        help_text="Current user status.",
        verbose_name="Status",
    )
    # Django built-in flags
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active.",
        verbose_name="Active",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can access the admin site.",
        verbose_name="Staff",
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
        verbose_name="Superuser",
    )

    # Custom manager for user creation
    objects = UserManager()

    # Set email as the unique identifier for authentication
    USERNAME_FIELD = "email"

    # REQUIRED_FIELDS should include any additional fields required during user creation via createsuperuser.
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        """Return the full name of the user."""
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()

        # If first or last name is missing, fallback to the email
        return self.email

    class Meta:
        db_table = "users"
        ordering = ["email"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email", "status"]),
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
        ]

    def __str__(self):
        return self.email


class Location(Timestamp):
    """Location model."""

    location_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="locations",
        help_text="User associated with this location.",
        verbose_name="User",
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="locations",
    )

    class Meta:
        db_table = "locations"
        # ordering = ["user"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.user.email}"


class Role(models.Model):
    class RoleNames(models.TextChoices):
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

    name = models.CharField(
        max_length=20,
        choices=RoleNames.choices,
        default=RoleNames.HOMEOWNER,
        unique=True,
        help_text="The name of the role.",
        verbose_name="Role Name",
    )

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class UserRole(Activity):
    """
    Junction model that links a user with a specific role and automatically creates an associated profile. This ensures a one-to-one relationship among the user, the role, and the profile.
    """

    # Link to the user to whom this role is assigned
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="role_assignments",
        help_text="User to whom this role is assigned.",
        verbose_name="User",
    )
    # Store the role using a CharField with limited choices
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        db_column="role_id",
        help_text="The role assigned to the user.",
        verbose_name="Role",
    )
    # One-to-one link to the associated profile
    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="profile_id",
        related_name="user_role",
        help_text="Profile automatically created for this role assignment.",
        verbose_name="Profile",
    )

    class Meta:
        db_table = "users_roles"
        ordering = ["user", "role"]  # Order by user then role
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                name="unique_user_role_assignment",
            )
        ]
        indexes = [
            # Composite index to speed up queries filtering by both user and role.
            models.Index(fields=["user", "role"]),
            # Separate index on profile for fast lookups.
            models.Index(fields=["profile"]),
        ]

    def save(self, *args, **kwargs):
        """Auto-create profile when role is assigned"""
        if not self.profile:
            self.profile = Profile.objects.create(role_assignment=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.role}"


class Profile(Timestamp):
    """User profile model."""

    profile_id = models.BigAutoField(
        primary_key=True,
        help_text="Unique identifier for the profile.",
        verbose_name="Profile ID",
    )
    # One-to-one relationship with UserRole, ensuring each role assignment has one profile.
    role_assignment = models.OneToOneField(
        "UserRole",
        on_delete=models.CASCADE,
        related_name="profile_link",
        help_text="The user role assignment linked to this profile.",
        verbose_name="Role Assignment",
    )
    # Organization to which the user is affiliated.
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="members",
        help_text="The organization this user profile is affiliated with.",
        verbose_name="Organization",
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Contact phone number.",
        verbose_name="Phone Number",
    )
    mobile_phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Mobile phone number.",
        verbose_name="Mobile Phone",
    )
    profile_picture = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="URL or path to the profile picture.",
        verbose_name="Profile Picture",
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="User's date of birth.",
        verbose_name="Date Of Birth",
    )
    # Many-to-many relationship with Language through an intermediary model.
    languages = models.ManyToManyField(
        "Language",
        through="ProfileLanguage",
        related_name="profiles",
        help_text="Languages known by the user.",
        verbose_name="Languages",
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Short biography of the user.",
        verbose_name="Biography",
    )
    cv = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Link or path to the user's CV.",
        verbose_name="Curriculum Vitae",
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The user's current job title.",
        verbose_name="Job Title",
    )
    address = models.OneToOneField(
        "Address",
        on_delete=models.CASCADE,
        db_column="address_id",
        blank=True,
        null=True,
        related_name="profiles",
        help_text="The address associated with this profile.",
        verbose_name="Address",
    )

    class Meta:
        db_table = "profiles"
        ordering = [
            "role_assignment__user__email"
        ]  # Order profiles by the user's email.
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["job_title"]),
            models.Index(fields=["date_of_birth"]),
        ]

    @property
    def user(self):
        """Access parent user through role assignment"""
        return self.role_assignment.user

    @property
    def role(self):
        """Access role through role assignment"""
        return self.role_assignment.get_role_display()

    def __str__(self):
        return f"{self.full_name}"


class ProfileLanguage(Timestamp):
    """Profile language model captures many-to-many relationship between user profiles and languages."""

    class ProficiencyLevels(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        FLUENT = "fluent", "Fluent"
        NATIVE = "native", "Native"

    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        db_column="profile_id",
        related_name="profile_languages",
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        db_column="language_id",
        related_name="language_profiles",
    )
    proficiency = models.CharField(
        max_length=20,
        choices=ProficiencyLevels.choices,
        default=ProficiencyLevels.FLUENT,
        help_text="Language proficiency level",
        verbose_name="Proficiency",
    )

    class Meta:
        db_table = "profile_languages"

    def __str__(self):
        return f"{self.profile.full_name} -> {self.language.name}"


class Address(Timestamp):
    """Address model."""

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0.0)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="addresses",
    )

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.country}"


class Language(models.Model):
    """Language model."""

    language_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, help_text="Language name")

    class Meta:
        db_table = "languages"

    def __str__(self):
        return self.name


# ============
# ORGANIZATION
# ============


class Organization(Activity):
    """Organization model."""

    organization_id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=255, unique=True, help_text="The name of the organization or firm."
    )
    description = models.TextField(
        blank=True, null=True, help_text="A short description of the organization."
    )
    address = models.ForeignKey(
        "Address",
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
    tags = GenericRelation(
        TaggedItem,
        related_query_name="otganizations",
    )

    class Meta:
        db_table = "organizations"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class Appliance(Timestamp):
    """Appliance model."""

    class ApplianceTypes(models.TextChoices):
        KITCHEN = "kitchen", "Kitchen"
        LAUNDRY = "laundry", "Laundry"
        HVAC = "hvac", "HVAC"
        WATER_HEATER = "water_heater", "Water Heater"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255, help_text="Name of the appliance.")
    description = models.TextField(
        blank=True, help_text="A brief description of the appliance."
    )
    brand = models.CharField(
        max_length=255,
        blank=True,
        help_text="The manufacturer or brand of the appliance.",
    )
    model = models.CharField(
        max_length=255, blank=True, help_text="The model designation or number."
    )
    serial_number = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
        help_text="The serial number of the appliance.",
    )
    tags = GenericRelation(
        TaggedItem,
        related_query_name="appliances",
    )

    class Meta:
        db_table = "appliances"
        ordering = ["name"]
        verbose_name = "Appliance"
        verbose_name_plural = "Appliances"

    def __str__(self):
        return self.name


class Property(Activity):
    """Property model representing a real estate property."""

    class PropertyTypes(models.TextChoices):
        HOUSE = "house", "House"
        APARTMENT = "apartment", "Apartment"
        CONDO = "condo", "Condo"
        TOWNHOUSE = "townhouse", "Townhouse"

    property_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, help_text="Title of the property listing.")
    description = models.TextField(help_text="Detailed description of the property.")
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
        "User",
        null=True,
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
        blank=True, null=True, help_text="Total area of the lot in square meters"
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
        blank=True, null=True, help_text="Total number of rooms in the property."
    )
    num_bathrooms = models.PositiveIntegerField(
        blank=True, null=True, help_text="Total number of bathrooms in the property."
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
        blank=True, null=True, help_text="The date when the property was built."
    )
    tax_assessed_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Property value as per the latest tax assessment.",
    )
    tax_annual_amount = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Annual property tax amount."
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
    tags = GenericRelation(
        TaggedItem,
        related_query_name="properties",
    )

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
        indexes = [
            models.Index(fields=["is_available", "is_published"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.title


class PropertyPhoto(Timestamp):
    """Property photo model."""

    photo_id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
        db_column="property_id",
    )
    photo_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="property_photos",
    )

    class Meta:
        db_table = "property_photos"

    def __str__(self):
        return f"{self.property.title} -> Photo {self.photo_id}"


class Amenity(Timestamp):
    """Amenity model."""

    amenity_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=10, decimal_places=7, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7, blank=True, null=True
    )
    tags = GenericRelation(
        TaggedItem,
        related_query_name="amenities",
    )

    class Meta:
        db_table = "amenities"

    def __str__(self):
        return self.name


class PropertyAmenity(models.Model):
    """Property amenity model captures many-to-many relationship between properties and amenities."""

    property = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
        db_column="property_id",
        related_name="property_amenities",
    )
    amenity = models.ForeignKey(
        "Amenity",
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


class OpenHouse(Activity):
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
        "Property",
        on_delete=models.CASCADE,
        db_column="property_id",
    )
    agents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="OpenHouseAgent",
        through_fields=("openhouse", "agent"),
        related_name="openhouses",
    )
    date = models.DateTimeField(null=True, blank=True)
    starttime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, default="in-person"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    notes = models.TextField(null=True, blank=True)
    attendees = models.TextField(null=True, blank=True)
    virtual_url = models.CharField(max_length=255, null=True, blank=True)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="openhouses",
    )

    class Meta:
        db_table = "openhouses"

    def __str__(self):
        return f"OpenHouse {self.property.title} - {self.date}"


class OpenHouseAgent(Activity):
    """Open house agent model captures many-to-many relationship between openhouses and agent users."""

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
        ("deleted", "Deleted"),
    )
    openhouse = models.ForeignKey(
        "OpenHouse", on_delete=models.CASCADE, db_column="openhouse_id"
    )
    agent = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        db_column="agent_id",
        related_name="agent_openhouses",
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    class Meta:
        db_table = "openhouse_agents"

    def __str__(self):
        return f"{self.openhouse.openhouse_id} - {self.status}"


class Booking(Activity):
    """Booking model."""

    booking_id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
        db_column="property_id",
    )
    guest = models.ForeignKey("User", on_delete=models.CASCADE, db_column="user_id")
    check_in = models.DateField(blank=True, null=True)
    check_out = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")
    tags = GenericRelation(
        TaggedItem,
        related_query_name="bookings",
    )

    class Meta:
        db_table = "bookings"

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property.title}"


class Payment(Activity):
    """Payment model."""

    payment_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, db_column="booking_id"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="pending")
    tags = GenericRelation(
        TaggedItem,
        related_query_name="payments",
    )

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking.booking_id}"


class BlockchainEvent(Timestamp):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=66)  # Blockchain transaction hash
    event_type = models.CharField(max_length=20)  # e.g., "NFT_MINT", "PAYMENT"
    timestamp = models.DateTimeField()
    tags = GenericRelation(
        TaggedItem,
        related_query_name="blockchain_events",
    )


class Review(Activity):
    """Review model."""

    review_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, db_column="booking_id"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="reviewer_id"
    )
    rating = (
        models.SmallIntegerField()
    )  # Alternatively, models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="reviews",
    )

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"Review {self.review_id} - Rating: {self.rating}"


class Favorite(Timestamp):
    """Favorite model."""

    favorite_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, db_column="property_id"
    )

    class Meta:
        db_table = "favorites"

    def __str__(self):
        return f"Favorite {self.favorite_id} by {self.user.email}"


class Message(Timestamp):
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
    is_read = models.BooleanField(default=False)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="messages",
    )

    class Meta:
        db_table = "messages"

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email} to {self.receiver.email}"


class Notification(Timestamp):
    """Notification model."""

    notification_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="notifications",
    )

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f"Notification {self.notification_id} for {self.user.email}"


class Product(models.Model):
    """Represents a product in the system."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    tags = GenericRelation(
        TaggedItem,
        related_query_name="products",
    )

    @property
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):
    """Represents an order in the system."""

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
        Product, through="OrderItem", related_name="orders"
    )
    tags = GenericRelation(
        TaggedItem,
        related_query_name="orders",
    )

    def __str__(self):
        return f"Order {self.order_id} by {self.user.email}"


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.URLField(max_length=255, blank=True)
    # Using RecipeTag for filtering recipes; note this is separate from frontend_tags.
    tags = models.ManyToManyField("RecipeTag")
    ingredients = models.ManyToManyField("Ingredient")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class RecipeTag(models.Model):
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
