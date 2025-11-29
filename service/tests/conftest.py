import pytest
from django.contrib.auth import get_user_model

from service.models import Airport, Route


# Airport
@pytest.fixture()
def create_airport_model(db):
    return Airport.objects.create(
        name="Airport",
        city="Hawkins",
        open_year=2025,
        image="image.png"
    )

@pytest.fixture()
def create_airport_list(db):
    raw_airports = [
        Airport(
            name="Airport Berlin",
            city="Berlin",
            open_year=2000,
            image="image-berlin-airport.png"
        ),
        Airport(
          name="Airport Paris",
          city="Paris",
          open_year=2001,
          image="image-paris-airport.png"
        ),
        Airport(
            name="Airport Kyiv",
            city="Kyiv",
            open_year=2002,
            image="image-kyiv-airport.png"
        )
    ]

    return Airport.objects.bulk_create(raw_airports)


# User
@pytest.fixture()
def create_admin_user(db):
    return get_user_model().objects.create_superuser(
        username="admin",
        password="adminpassword"
    )

@pytest.fixture()
def create_user(db):
    return get_user_model().objects.create_user(
        username="user",
        password="userpassword"
    )


# Route
@pytest.fixture()
def create_route(db, create_airport_list):
    airports = create_airport_list

    return Route.objects.create(
        source=airports[0],
        destination=airports[1],
        distance=10,
    )

