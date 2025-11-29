from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient, APIRequestFactory

from ..conftest import create_admin_user, create_user, create_airport_list, create_airport_model
from ..utils import get_test_image
from ...serializers import AirportSerializer, AirportImageSerializer

from service.models import Airport

AIRPORT_LIST_URL = reverse_lazy("service:airports-list")

class TestPrivateAirportListView:
    def setup_method(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.request = self.factory.get(AIRPORT_LIST_URL)

    def test_airport_list(self, create_admin_user, create_airport_list):
        user = create_admin_user
        self.client.force_authenticate(user)

        airport_list = sorted(
            create_airport_list,
            key=lambda i: i.created_at,
            reverse=True
        )

        airport_serializer = AirportSerializer(
            airport_list,
            many=True,
            context={"request": self.request}
        )

        response = self.client.get(AIRPORT_LIST_URL)


        assert response.status_code == status.HTTP_200_OK
        assert response.data == airport_serializer.data


    def test_airport_list_should_be_filtered_by_city_query_params(self, create_admin_user, create_airport_list):
        airport_list = sorted(
            create_airport_list,
            key=lambda i: i.created_at,
            reverse=True
        )
        user = create_admin_user

        self.client.force_authenticate(user)

        response = self.client.get(AIRPORT_LIST_URL, {"city": "Berlin,Paris"})
        airport_serializer = AirportSerializer(
            airport_list,
            many=True,
            context={"request": self.request
        })

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        assert response.data == [airport_serializer.data[1], airport_serializer.data[2]]


    def test_airport_list_should_be_filtered_by_year_query_params(self, create_admin_user, create_airport_list):
        airport_list = sorted(
            create_airport_list,
            key=lambda i: i.created_at,
            reverse=True
        )
        user = create_admin_user

        self.client.force_authenticate(user)

        response = self.client.get(AIRPORT_LIST_URL, {"year": "2000,2001"})
        airport_serializer = AirportSerializer(
            airport_list,
            many=True,
            context={"request": self.request
        })

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        assert response.data == [airport_serializer.data[1], airport_serializer.data[2]]

    def test_airport_post(self, create_admin_user):
        user = create_admin_user
        self.client.force_authenticate(user)

        airport_data = {
            "name": "Airport",
            "city": "Hawkins",
            "open_year": 2025,
        }

        response = self.client.post(AIRPORT_LIST_URL, airport_data)

        airport = Airport.objects.get(id=response.data["id"])
        airport_serializer = AirportSerializer(airport)

        assert response.status_code == status.HTTP_201_CREATED
        assert Airport.objects.count() == 1

        assert response.data == airport_serializer.data


class TestPublicAirportListView:
    def setup_method(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.request = self.factory.get(AIRPORT_LIST_URL)

    def test_public_airport_list(self, create_user, create_airport_list):
        user = create_user
        self.client.force_authenticate(user)

        airport_list = sorted(
            create_airport_list,
            key=lambda i:i.created_at,
            reverse=True
        )

        airport_serializer = AirportSerializer(
            airport_list,
            many=True,
            context={"request": self.request}
        )
        response = self.client.get(AIRPORT_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == airport_serializer.data


    def test_public_airport_post_should_not_create_object(self, create_user):
        user = create_user
        self.client.force_authenticate(user)

        airport_data = {
            "name": "Airport",
            "city": "Hawkins",
            "open_year": 2025,
        }

        response = self.client.post(AIRPORT_LIST_URL, airport_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPrivateAirportDetailView:
    def setup_method(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_airport_detail(self, create_admin_user, create_airport_model):
        user = create_admin_user
        self.client.force_authenticate(user)

        airport = create_airport_model
        url = reverse_lazy("service:airports-detail", args=[airport.id])
        self.request = self.factory.get(url)

        airport_serializer = AirportSerializer(airport, context={"request": self.request})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == airport_serializer.data


    def test_airport_upload_image(self, create_admin_user, create_airport_model):
        user = create_admin_user
        self.client.force_authenticate(user)

        airport = create_airport_model
        image_file = get_test_image()

        url = reverse_lazy("service:airports-upload-image", args=[airport.id])
        response = self.client.post(url, {"image": image_file}, format="multipart")

        airport.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["image"].endswith(str(airport.image))



class TestPublicAirportDetailView:
    def setup_method(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_airport_upload_image(self, create_user, create_airport_model):
        user = create_user
        self.client.force_authenticate(user)

        airport = create_airport_model
        image_file = get_test_image()

        url = reverse_lazy("service:airports-upload-image", args=[airport.id])
        response = self.client.post(url, {"image": image_file}, format="multipart")

        assert response.status_code == status.HTTP_403_FORBIDDEN
