from django.db import models
from django.db.models import UniqueConstraint

from .utils import create_airport_image_url

class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
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


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_source"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_destination"
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.distance}km.)"

    class Meta:
        ordering = ["distance"]
        verbose_name_plural = "Routes"
        verbose_name = "Route"
        constraints = [
            UniqueConstraint(
                fields=["source", "destination"],
                name="unique_route"
            )
        ]
