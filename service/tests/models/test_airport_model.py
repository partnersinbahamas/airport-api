import pytest
from django.db import IntegrityError, transaction

from ..fixtures import create_airport_model
from ...models import Airport


class TestAirportModel:
    def test_airport_model_should_be_created(self, create_airport_model):
        airport = create_airport_model

        assert airport.name == "Airport"
        assert airport.city == "Hawkins"
        assert airport.open_year == 2025
        assert airport.image == "image.png"
        assert str(airport) == "Airport (2025)"


    def test_airport_model_name_should_be_unique(self, create_airport_model):
        airport_1 = create_airport_model

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                airport_2 = Airport.objects.create(
                    name="Airport",
                    city="Hawkins",
                    open_year=2025,
                    image="image.png"
                )

        assert Airport.objects.count() == 1

