import pytest
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from rest_framework.test import APIClient

from ..factories import UserFactory

from service.views import ManufacturerCreateSerializer
from ...models import Manufacturer

MANUFACTURER_VIEW_URL = reverse_lazy('service:manufacturers-list')

@pytest.mark.django_db
class TestPrivateManufacturerViews:
    def setup_method(self):
        self.client = APIClient()

    def test_manufacturer_should_be_created(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        manufacturer_data = {"name": "Manufacturer", "country": "USU"}

        response = self.client.post(MANUFACTURER_VIEW_URL, manufacturer_data)

        manufacturer = Manufacturer.objects.get(id=response.data["id"])
        serializer = ManufacturerCreateSerializer(manufacturer)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == serializer.data["name"]
        assert response.data["country"] == serializer.data["country"]
        assert serializer.data["airplanes"] == []


@pytest.mark.django_db
class TestPublicManufacturerViews:
    def setup_method(self):
        self.client = APIClient()

    def test_manufacturer_should_not_be_created(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        manufacturer_data = {"name": "Manufacturer", "country": "USU"}

        response = self.client.post(MANUFACTURER_VIEW_URL, manufacturer_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN