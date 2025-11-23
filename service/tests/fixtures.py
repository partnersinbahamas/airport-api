import pytest

from service.models import Airport


@pytest.fixture()
def create_airport_model(db):
    return Airport.objects.create(
        name="Airport",
        city="Hawkins",
        open_year=2025,
        image="image.png"
    )