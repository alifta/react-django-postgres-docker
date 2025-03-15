from django.db import models


class Restaurant(models.Model):
    """Restaurant model."""

    name = models.CharField(max_length=100)
    website = models.URLField(max_length=255, blank=True, null=True)
    date_opened = models.DateField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "restaurants"

    def __str__(self):
        return self.name
