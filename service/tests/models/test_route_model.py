import pytest
from django.db import transaction, IntegrityError

from service.models import Route

from ..factories import AirportFactory, RouteFactory

@pytest.mark.django_db
class TestRouteModel:
    def test_route_model_should_be_created(self):
        berlin_airport = AirportFactory(name="Airport Berlin", open_year=2000)
        paris_airport = AirportFactory(name="Airport Paris", open_year=2001)

        route = RouteFactory(
            source=berlin_airport,
            destination=paris_airport,
            distance=10
        )

        assert route.source.name == "Airport Berlin"
        assert route.destination.name == "Airport Paris"
        assert route.distance == 10

        assert str(route) == "Airport Berlin (2000) - Airport Paris (2001) (10km.)"

    def test_route_should_be_unique(self):
        berlin_airport = AirportFactory(name="Airport Berlin", open_year=2000)
        paris_airport = AirportFactory(name="Airport Paris", open_year=2001)

        _route_1 = RouteFactory(
            source=berlin_airport,
            destination=paris_airport,
            distance=10
        )

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                _route_2 = RouteFactory(
                    source=berlin_airport,
                    destination=paris_airport,
                    distance=10
                )

        assert Route.objects.count() == 1
