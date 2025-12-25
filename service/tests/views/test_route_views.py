import pytest

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from ..factories import AirportFactory, UserFactory
from ...serializers import RouteRetrieveSerializer
from ...models import Route

ROUTE_VIEW_URL = reverse_lazy("service:routes-list")


@pytest.mark.django_db
class TestPrivateRouteView:
    def setup_method(self):
        self.client = APIClient()

    def test_route_should_be_created(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        source = AirportFactory()
        destination = AirportFactory()

        route_data = {
            "source": source.id,
            "destination": destination.id,
            "distance": 20,
        }

        response = self.client.post(ROUTE_VIEW_URL, route_data)

        route = Route.objects.get(id=response.data["id"])
        route_serializer = RouteRetrieveSerializer(route)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == route_serializer.data


    def test_route_should_not_be_created_if_source_and_destination_are_the_same(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        source = AirportFactory(name="Airport 1")

        route_data = {
            "source": source.id,
            "destination": source.id,
            "distance": 20,
        }

        response = self.client.post(ROUTE_VIEW_URL, route_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Source and destination cannot be the same." in response.data["detail"]


@pytest.mark.django_db
class TestPublicRouteView:
    def setup_method(self):
        self.client = APIClient()

    def test_route_should_not_be_created(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        source = AirportFactory()
        destination = AirportFactory()

        route_data = {
            "source": source.id,
            "destination": destination.id,
            "distance": 20,
        }

        response = self.client.post(ROUTE_VIEW_URL, route_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
