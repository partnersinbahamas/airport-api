import pytest

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from ..factories import (
    UserFactory,
    FlightFactory,
    AirplaneFactory,
    CrewFactory,
    RouteFactory,
)
from ...serializers import FlightReadSerializer

from service.choices import CrewTypeChoices
from service.models import Flight

FLIGHT_VIEW_LIST_URL = reverse_lazy("service:flights-list")

@pytest.mark.django_db
class TestPublicFlightViews:
    def setup_method(self):
        self.client = APIClient()
        admin = UserFactory(admin=True)
        self.client.force_authenticate(admin)


    def test_flight_should_be_created(self):
        airplane = AirplaneFactory(pilots_capacity=2, personal_capacity=2)
        route = RouteFactory()

        flight_crew_1 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)
        flight_crew_2 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)

        cabin_crew_1 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)
        cabin_crew_2 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)


        flight_data = {
            "route": route.pk,
            "airplane": airplane.pk,
            "crew": [
                flight_crew_1.pk,
                flight_crew_2.pk,
                cabin_crew_1.pk,
                cabin_crew_2.pk
            ],
            "departure_time": "2022-01-01T12:00:00Z",
            "arrival_time": "2022-01-01T12:30:00Z",
        }

        response = self.client.post(FLIGHT_VIEW_LIST_URL, flight_data)

        flight = Flight.objects.get(id=response.data["id"])
        flight_serializer = FlightReadSerializer(flight)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == flight_serializer.data


    def test_flight_should_validate_minimal_pilots_capacity(self):
        airplane = AirplaneFactory(pilots_capacity=2, personal_capacity=2)
        route = RouteFactory()

        flight_crew_1 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)

        cabin_crew_1 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)
        cabin_crew_2 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)


        flight_data = {
            "route": route.pk,
            "airplane": airplane.pk,
            "crew": [flight_crew_1.pk, cabin_crew_1.pk, cabin_crew_2.pk],
            "departure_time": "2022-01-01T12:00:00Z",
            "arrival_time": "2022-01-01T12:30:00Z",
        }

        response = self.client.post(FLIGHT_VIEW_LIST_URL, flight_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "The number of airline pilots capacity must be at least 2." in response.data["non_field_errors"]


    def test_flight_should_validate_maximal_pilots_capacity(self):
        airplane = AirplaneFactory(pilots_capacity=2, personal_capacity=2)
        route = RouteFactory()

        flight_crew_1 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)
        flight_crew_2 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)
        flight_crew_3 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)

        cabin_crew_1 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)
        cabin_crew_2 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)


        flight_data = {
            "route": route.pk,
            "airplane": airplane.pk,
            "crew": [
                flight_crew_1.pk,
                flight_crew_2.pk,
                flight_crew_3.pk,
                cabin_crew_1.pk,
                cabin_crew_2.pk
            ],
            "departure_time": "2022-01-01T12:00:00Z",
            "arrival_time": "2022-01-01T12:30:00Z",
        }

        response = self.client.post(FLIGHT_VIEW_LIST_URL, flight_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "The number of flight crew exceeds the airline's pilot capacity." in response.data["non_field_errors"]


    def test_flight_should_validate_minimal_personal_capacity(self):
        airplane = AirplaneFactory(pilots_capacity=2, personal_capacity=2)
        route = RouteFactory()

        flight_crew_1 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)
        flight_crew_2 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)

        cabin_crew_1 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)


        flight_data = {
            "route": route.pk,
            "airplane": airplane.pk,
            "crew": [
                flight_crew_1.pk,
                flight_crew_2.pk,
                cabin_crew_1.pk,
            ],
            "departure_time": "2022-01-01T12:00:00Z",
            "arrival_time": "2022-01-01T12:30:00Z",
        }

        response = self.client.post(FLIGHT_VIEW_LIST_URL, flight_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "The number of airline personal capacity must be at least 2." in response.data["non_field_errors"]


    def test_flight_should_validate_maximal_personal_capacity(self):
        airplane = AirplaneFactory(pilots_capacity=2, personal_capacity=2)
        route = RouteFactory()

        flight_crew_1 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)
        flight_crew_2 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)

        cabin_crew_1 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)
        cabin_crew_2 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)
        cabin_crew_3 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)


        flight_data = {
            "route": route.pk,
            "airplane": airplane.pk,
            "crew": [
                flight_crew_1.pk,
                flight_crew_2.pk,
                cabin_crew_1.pk,
                cabin_crew_2.pk,
                cabin_crew_3.pk
            ],
            "departure_time": "2022-01-01T12:00:00Z",
            "arrival_time": "2022-01-01T12:30:00Z",
        }

        response = self.client.post(FLIGHT_VIEW_LIST_URL, flight_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "The number of cabin crew exceeds the airline's personal capacity." in response.data["non_field_errors"]


    def test_flight_view_should_be_paginated(self):
        flights_count = 10
        FlightFactory.create_batch(flights_count)

        response = self.client.get(FLIGHT_VIEW_LIST_URL)

        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == flights_count
        assert "service/flights/?page=2" in response.data["next"]
        assert len(response.data["results"]) == 5


