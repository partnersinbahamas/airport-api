from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint, Q, F, CheckConstraint

from .constants import MAX_PILOT_CAPACITY
from .utils import (
    create_airport_image_url,
    create_manufacturer_logo_url,
    create_airplane_image_url
)
from .choices import (
    CrewTypeChoices,
    CREW_POSITION_CHOICES_LIST,
    FlightCrewPositionChoices,
    CabinCrewPositionChoices
)


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
            ),
            CheckConstraint(
                check=~Q(source=F("destination")),
                name="source_not_equal_destination",
            )
        ]


class Manufacturer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50)
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(null=True, upload_to=create_manufacturer_logo_url)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.country})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Manufacturers"
        verbose_name = "Manufacturer"


class AirplaneType(models.Model):
    name = models.CharField(max_length=50,unique=True)
    code = models.CharField(max_length=3, unique=True)
    purpose = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name_plural = "Airplane Types"
        verbose_name = "Airplane Type"
        ordering = ["code"]


class Airplane(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(AirplaneType, on_delete=models.PROTECT, related_name="airplanes")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name="airplanes")
    rows = models.PositiveSmallIntegerField(null=True, blank=True)
    seats_in_row = models.PositiveSmallIntegerField(null=True, blank=True)
    pilots_capacity = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(MAX_PILOT_CAPACITY),
            MinValueValidator(1)
        ]
    )
    personal_capacity = models.PositiveSmallIntegerField(default=0)
    year_of_manufacture = models.PositiveSmallIntegerField()
    fuel_capacity_l = models.PositiveIntegerField()
    cargo_capacity_kg = models.PositiveIntegerField()
    max_speed_kmh = models.PositiveIntegerField()
    max_distance_km = models.PositiveIntegerField()
    image = models.ImageField(null=True, upload_to=create_airplane_image_url)

    def __str__(self):
        return f"{self.name} - {self.type.code}"

    @property
    def crew_capacity(self):
        return self.personal_capacity + self.pilots_capacity

    @property
    def passenger_seats_total(self):
        if not self.rows or not self.seats_in_row:
            return 0

        return self.rows * self.seats_in_row

    @property
    def seats_total(self):
        return self.passenger_seats_total + self.crew_capacity


    class Meta:
        ordering = ["year_of_manufacture"]
        verbose_name_plural = "Airplanes"
        verbose_name = "Airplane"



class Crew(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    crew_type = models.CharField(choices=CrewTypeChoices.choices, max_length=20)
    position = models.CharField(choices=CREW_POSITION_CHOICES_LIST, max_length=30)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]

    @property
    def position_label(self):
        if self.position:
            return dict(CREW_POSITION_CHOICES_LIST).get(self.position)

        return None

    @property
    def crew_type_label(self):
        if self.crew_type:
            return dict(CrewTypeChoices.choices)[self.crew_type]

        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.crew_type_label}, {self.position_label})"


    def clean(self):
        super().clean()

        if self.crew_type and self.position:
            if self.crew_type == CrewTypeChoices.FLIGHT_CREW and self.position not in FlightCrewPositionChoices:
                raise ValidationError(f"Invalid {self.position_label} position for flight crew.")
            elif self.crew_type == CrewTypeChoices.CABIN_CREW and self.position not in CabinCrewPositionChoices:
                raise ValidationError(f"Invalid {self.position_label} position for cabin crew.")


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.PROTECT,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self):
        return f"{self.route} - {self.airplane}"

    class Meta:
        verbose_name_plural = "Flights"
        verbose_name = "Flight"
        ordering = ["departure_time"]
