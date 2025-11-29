import pytest
from django.db import transaction, IntegrityError

from service.models import Route

from ..conftest import create_route, create_airport_list


class TestRouteModel:
    def test_route_model_should_be_created(self, create_route):
        route = create_route

        assert route.source.name == "Airport Berlin"
        assert route.destination.name == "Airport Paris"
        assert route.distance == 10

        assert str(route) == "Airport Berlin (2000) - Airport Paris (2001) (10km.)"

    def test_route_should_be_unique(self, create_route, create_airport_list):
        _route_1 = create_route

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                airports = create_airport_list
                _route_2 = Route.objects.create(
                    source=airports[0],
                    destination=airports[1],
                    distance=20,
                )

        assert Route.objects.count() == 1
