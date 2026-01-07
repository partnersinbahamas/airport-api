import pytest
from django.core.exceptions import ValidationError
from django.db import transaction

from ..factories import TicketFactory, AirplaneFactory, FlightFactory, OrderFactory, UserFactory
from service.models import Ticket


@pytest.mark.django_db
class TestTicketModel:
    def test_ticket_should_be_created(self):
        airplane = AirplaneFactory(name="Airplane-1", rows=10, seats_in_row=6)
        user = UserFactory(username="John Doe")
        order = OrderFactory(user=user)
        flight = FlightFactory(airplane=airplane)

        ticket = TicketFactory(flight=flight, order=order, row=10, seat=1)

        assert ticket.flight.airplane.name == airplane.name
        assert ticket.order.user.username == user.username
        assert ticket.row == 10
        assert ticket.seat == 1


    def test_ticket_should_validate_booked_seat(self):
        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        ticket_1 = TicketFactory(flight=flight, row=10, seat=1)
        ticket_1.full_clean()

        with transaction.atomic():
            with pytest.raises(ValidationError) as exception:
                order = OrderFactory()
                ticket_2 = TicketFactory.build(flight=flight, order=order, row=10, seat=1)
                ticket_2.full_clean()

        errors = exception.value.message_dict

        assert Ticket.objects.count() == 1
        assert "Ticket with this Row, Seat and Flight already exists." in errors["__all__"]


    def test_ticket_should_validate_max_value_of_airplane_rows(self):
        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        with transaction.atomic():
            with pytest.raises(ValidationError) as exception:
                order = OrderFactory()
                ticket_1 = TicketFactory.build(flight=flight, order=order, row=11, seat=1)
                ticket_1.full_clean()

        errors = exception.value.message_dict

        assert not Ticket.objects.exists()
        assert "Invalid row number. Row number must be between 1 and 10." in errors["__all__"]


    def test_ticket_should_validate_max_value_of_airplane_seats_in_row(self):
        airplane = AirplaneFactory(rows=10, seats_in_row=6)
        flight = FlightFactory(airplane=airplane)

        with transaction.atomic():
            with pytest.raises(ValidationError) as exception:
                order = OrderFactory()
                ticket_1 = TicketFactory.build(flight=flight, order=order, row=10, seat=8)
                ticket_1.full_clean()

        errors = exception.value.message_dict

        assert not Ticket.objects.exists()
        assert "Invalid seat number. Seat number must be between 1 and 6." in errors["__all__"]


    def test_ticket_should_not_be_booked_for_airplane_with_no_seats_or_rows(self):
        airplane = AirplaneFactory(name="Airplane-1",  rows=None, seats_in_row=None)
        flight = FlightFactory(airplane=airplane)

        with transaction.atomic():
            with pytest.raises(ValidationError) as exception:
                order = OrderFactory()
                ticket_1 = TicketFactory.build(flight=flight, order=order, row=10, seat=6)
                ticket_1.full_clean()


        errors = exception.value.message_dict

        assert not Ticket.objects.exists()
        assert "Ticket cannot be booked for Airplane-1." in errors["__all__"]
