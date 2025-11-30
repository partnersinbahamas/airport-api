import pytest

from django.db import IntegrityError, transaction

from ...models import Airport
from ..factories import AirportFactory

@pytest.mark.django_db
class TestAirportModel:
    def test_airport_model_should_be_created(self):
        airport = AirportFactory(
            name="Airport",
            city="Hawkins",
            open_year=2025,
            image="image.png",
        )

        assert airport.name == "Airport"
        assert airport.city == "Hawkins"
        assert airport.open_year == 2025
        assert airport.image == "image.png"
        assert str(airport) == "Airport (2025)"


    def test_airport_model_name_should_be_unique(self):
        _airport_1 = AirportFactory(name="Airport")

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                _airport_2 = AirportFactory(name="Airport")

        assert Airport.objects.count() == 1
