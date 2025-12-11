import pytest
from django.db import transaction, IntegrityError

from ..factories import ManufacturerFactory
from ...models import Manufacturer


@pytest.mark.django_db
class TestManufacturerModel:
    def test_manufacturer_model_should_be_created(self):
        manufacturer = ManufacturerFactory(
            name="Manufacturer",
            country="USU",
            founded_year=2000,
            website="https://www.manufacturer.com",
            logo="USU-logo.png"
        )

        assert manufacturer.name == "Manufacturer"
        assert manufacturer.country == "USU"
        assert manufacturer.founded_year == 2000
        assert manufacturer.website == "https://www.manufacturer.com"
        assert manufacturer.logo == "USU-logo.png"


    def test_manufacturer_model_name_should_be_unique(self):
        _manufacturer_1 = ManufacturerFactory(
            name="Manufacturer",
        )

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                _manufacturer_2 = ManufacturerFactory(
                    name="Manufacturer",
                )

        assert Manufacturer.objects.count() == 1
