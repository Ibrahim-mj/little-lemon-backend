from django.db import models

class Location(models.Model):
    """
    A model for handling locations.
    """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=6, decimal_places=6)
    longitude = models.DecimalField(max_digits=6, decimal_places=6)
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name
