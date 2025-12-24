import pytest

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from service.models import Airplane

from ..factories import UserFactory, ManufacturerFactory, AirplaneTypeFactory, AirplaneFactory
from ..utils import get_test_image
from ...serializers import AirplaneRetrieveSerializer, AirplaneListSerializer


AIRPLANE_VIEW_URL = reverse_lazy("service:airplanes-list")

@pytest.mark.django_db
class TestPrivateAirplaneViews:
    def setup_method(self):
        self.client = APIClient()


    def test_airplane_should_be_created(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        manufacturer = ManufacturerFactory(name="Manufacturer")
        airplane_type = AirplaneTypeFactory(name="Airplane A380", code="AA1")
        image_file = get_test_image()

        airplane_data = {
            "name": "Airplane",
            "manufacturer": manufacturer.pk,
            "type": airplane_type.pk,
            "rows": 16,
            "seats_in_row": 6,
            "pilots_capacity": 2,
            "personal_capacity": 4,
            "year_of_manufacture": 2020,
            "fuel_capacity_l": 10000,
            "cargo_capacity_kg": 10000,
            "max_speed_kmh": 100,
            "max_distance_km": 10000,
            "image": image_file,
        }

        response = self.client.post(AIRPLANE_VIEW_URL, data=airplane_data)

        airplane = Airplane.objects.get(id=response.data["id"])
        serializer = AirplaneRetrieveSerializer(airplane)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == serializer.data


@pytest.mark.django_db
class TestPublicAirplaneViews:
    def setup_method(self):
        self.client = APIClient()


    def test_airplane_list_should_be_filtered_by_name(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        _airplane_1 = AirplaneFactory(name="Airplane 1", year_of_manufacture=2020)
        _airplane_2 = AirplaneFactory(name="Airplane 2", year_of_manufacture=2021)

        response = self.client.get(AIRPLANE_VIEW_URL, {"name": "Airplane 1"})

        airplane_list = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane_list, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [serializer.data[0]]


    def test_airplane_list_should_be_filtered_by_year(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        _airplane_1 = AirplaneFactory(year_of_manufacture=2020)
        _airplane_2 = AirplaneFactory(year_of_manufacture=2021)
        _airplane_3 = AirplaneFactory(year_of_manufacture=2022)

        response = self.client.get(AIRPLANE_VIEW_URL, {"year": "2022,2021"})

        airplane_list = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane_list, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [serializer.data[1], serializer.data[2]]


    def test_airplane_list_should_be_filtered_by_manufacturer_name(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        manufacturer_1 = ManufacturerFactory(name="Manufacturer 1")
        manufacturer_2 = ManufacturerFactory(name="Manufacturer 2")

        _airplane_1 = AirplaneFactory(manufacturer=manufacturer_1, year_of_manufacture=2020)
        _airplane_2 = AirplaneFactory(manufacturer=manufacturer_2, year_of_manufacture=2021)

        response = self.client.get(AIRPLANE_VIEW_URL, {"manufacturer": "Manufacturer 1"})

        airplane_list = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane_list, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [serializer.data[0]]


    def test_airplane_list_should_be_filtered_by_type(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        airplane_type_1 = AirplaneTypeFactory(name="Commercial", code="COM")
        airplane_type_2 = AirplaneTypeFactory(name="Cargo", code="CGO")

        _airplane_1 = AirplaneFactory(type=airplane_type_1, year_of_manufacture=2020)
        _airplane_2 = AirplaneFactory(type=airplane_type_2, year_of_manufacture=2021)

        response = self.client.get(AIRPLANE_VIEW_URL, {"type": "Cargo"})

        airplane_list = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane_list, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [serializer.data[1]]


    def test_airplane_should_not_be_created(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        manufacturer = ManufacturerFactory(name="Manufacturer")
        airplane_type = AirplaneTypeFactory(name="Airplane A380", code="AA1")
        image_file = get_test_image()

        airplane_data = {
            "name": "Airplane",
            "manufacturer": manufacturer.pk,
            "type": airplane_type.pk,
            "rows": 16,
            "seats_in_row": 6,
            "pilots_capacity": 2,
            "personal_capacity": 4,
            "year_of_manufacture": 2020,
            "fuel_capacity_l": 10000,
            "cargo_capacity_kg": 10000,
            "max_speed_kmh": 100,
            "max_distance_km": 10000,
            "image": image_file,
        }

        response = self.client.post(AIRPLANE_VIEW_URL, data=airplane_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
