from django.db import models

from .utils import create_airport_image_url

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=55)
    image = models.ImageField(null=True, upload_to=create_airport_image_url)
    open_year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.open_year})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Airports"
        verbose_name = "Airport"
