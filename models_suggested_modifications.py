# models.py (Additions/Modifications)


class Foundation(models.Model):
    """Details about property foundation"""

    FOUNDATION_TYPES = [
        ("slab", "Slab"),
        ("crawl", "Crawl Space"),
        ("basement", "Basement"),
        ("pillar", "Pillar"),
    ]

    property = models.OneToOneField(
        Property, on_delete=models.CASCADE, related_name="foundation_details"
    )
    foundation_type = models.CharField(
        max_length=20,
        choices=FOUNDATION_TYPES,
        help_text="Type of foundation structure",
    )
    material = models.CharField(
        max_length=100, help_text="Primary construction material used"
    )
    waterproofing = models.BooleanField(
        default=False, help_text="Presence of waterproofing system"
    )


class CoolingType(models.Model):
    """Types of cooling systems available"""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class HeatingType(models.Model):
    """Types of heating systems available"""

    name = models.CharField(max_length=50, unique=True)
    fuel_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Property(models.Model):
    # Existing fields...

    # New scalar fields
    above_grade_finished_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Finished area above ground surface",
    )
    attached_garage_yn = models.BooleanField(
        default=False, help_text="Whether garage is attached to dwelling"
    )
    year_built = models.PositiveIntegerField(
        null=True, blank=True, help_text="Year of initial construction completion"
    )
    living_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total livable area including all floors",
    )

    # New relationship fields
    cooling_systems = models.ManyToManyField(
        CoolingType, blank=True, help_text="Available cooling system types"
    )
    heating_systems = models.ManyToManyField(
        HeatingType, blank=True, help_text="Available heating system types"
    )
    accessibility_features = models.ManyToManyField(
        "AccessibilityFeature", blank=True, help_text="List of accessibility features"
    )
    architectural_styles = models.ManyToManyField(
        "ArchitecturalStyle", blank=True, help_text="Architectural design styles"
    )


class AccessibilityFeature(models.Model):
    """Accessibility features for properties"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ArchitecturalStyle(models.Model):
    """Architectural design styles"""

    STYLE_CHOICES = [
        ("victorian", "Victorian"),
        ("ranch", "Ranch"),
        ("contemporary", "Contemporary"),
        ("craftsman", "Craftsman"),
    ]

    name = models.CharField(max_length=50, choices=STYLE_CHOICES, unique=True)
    era = models.CharField(max_length=50, help_text="Historical era of the style")

    def __str__(self):
        return self.get_name_display()


class Utility(models.Model):
    """Property utility information"""

    property = models.OneToOneField(
        Property, on_delete=models.CASCADE, related_name="utilities"
    )
    sewer_type = models.CharField(max_length=50, help_text="Type of sewer system")
    water_source = models.CharField(max_length=50, help_text="Primary water source")
    electric_service = models.CharField(
        max_length=50, help_text="Type of electrical service"
    )


class GreenCertification(models.Model):
    """Green building certifications"""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="green_certifications"
    )
    certification_type = models.CharField(
        max_length=50,
        choices=[
            ("leed", "LEED"),
            ("energy_star", "Energy Star"),
            ("green_globes", "Green Globes"),
        ],
    )
    rating = models.CharField(max_length=20, help_text="Certification level/rating")
    year_achieved = models.PositiveIntegerField()


class TaxInformation(models.Model):
    """Property tax details"""

    property = models.OneToOneField(
        Property, on_delete=models.CASCADE, related_name="tax_info"
    )
    annual_amount = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Yearly property tax amount"
    )
    assessed_value = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Most recent assessed value"
    )
    exemptions = models.JSONField(
        default=list, help_text="List of applicable tax exemptions"
    )
