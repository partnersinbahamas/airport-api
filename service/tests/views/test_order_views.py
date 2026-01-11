import pytest
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from service.models import Ticket, Order
from service.serializers import OrderReadSerializer

from ..factories import UserFactory, FlightFactory, AirplaneFactory


ORDER_LIST_VIEW_URL = reverse_lazy("service:orders-list")

@pytest.mark.django_db
class TestPrivateOrderViews:
    def setup_method(self):
        self.client = APIClient()

    def test_order_view_should_validate_tickets_data(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        order_data = {
            "tickets": [
                {
                    "row": 11,
                    "seat": 5,
                    "flight": flight.id
                }
           ]
        }

        response = self.client.post(ORDER_LIST_VIEW_URL, data=order_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert  "Invalid row number. Row number must be between 1 and 10." in response.data["tickets"][0]['non_field_errors'] # ??

    def test_order_should_be_created_with_tickets_and_admin_user(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        order_data = {
            "tickets": [
                {
                    "row": 9,
                    "seat": 5,
                    "flight": flight.id
                }
           ]
        }

        response = self.client.post(ORDER_LIST_VIEW_URL, data=order_data, format='json')

        created_ticket_id = response.data['tickets'][0]['id']
        created_order_id = response.data['id']
        order_user = response.data['user']

        ticket = Ticket.objects.get(id=created_ticket_id)
        order = Order.objects.get(id=created_order_id)

        serializer = OrderReadSerializer(order)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == serializer.data

        assert order_user == user.id

        assert Ticket.objects.count() == 1
        assert ticket.row == 9
        assert ticket.seat == 5
        assert ticket.flight.id == flight.id
        assert ticket.order.id == created_order_id


@pytest.mark.django_db
class TestPublicOrderViews:
    def setup_method(self):
        self.client = APIClient()

    def test_should_not_be_created_with_anonymous_user(self):
        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        order_data = {
            "tickets": [
                {
                    "row": 9,
                    "seat": 5,
                    "flight": flight.id
                }
           ]
        }

        response = self.client.post(ORDER_LIST_VIEW_URL, data=order_data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_order_should_be_created_with_tickets_and_authenticated_user(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        order_data = {
            "tickets": [
                {
                    "row": 9,
                    "seat": 5,
                    "flight": flight.id
                }
           ]
        }

        response = self.client.post(ORDER_LIST_VIEW_URL, data=order_data, format='json')

        created_ticket_id = response.data['tickets'][0]['id']
        created_order_id = response.data['id']
        order_user = response.data['user']

        ticket = Ticket.objects.get(id=created_ticket_id)
        order = Order.objects.get(id=created_order_id)

        serializer = OrderReadSerializer(order)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == serializer.data

        assert order_user == user.id

        assert Ticket.objects.count() == 1
        assert ticket.row == 9
        assert ticket.seat == 5
        assert ticket.flight.id == flight.id
        assert ticket.order.id == created_order_id
