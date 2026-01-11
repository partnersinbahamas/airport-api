import factory
import random
from django.contrib.auth import get_user_model

from ..constants import MAX_PILOT_CAPACITY
from ..models import Airport, Route, AirplaneType, Manufacturer, Airplane, Crew, Flight, Order, Ticket
from ..utils import generate_unique_letters_code
from ..choices import (
    CrewTypeChoices,
    FlightCrewPositionChoices,
    CabinCrewPositionChoices
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall(
        "set_password",
        "userpassword"
    )
    is_staff = False
    is_superuser = False

    class Params:
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True
        )


class AirportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Airport

    name = factory.Faker("name")
    city = factory.Faker("city")
    open_year = factory.Faker("year")

    image = None


class RouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Route

    source = factory.SubFactory(AirportFactory)
    destination = factory.SubFactory(AirportFactory)
    distance = factory.Faker("pyint")


class AirplaneTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AirplaneType

    name = factory.Faker("name")
    code = factory.Sequence(lambda n: generate_unique_letters_code(n))
    purpose = factory.Faker("sentence")


class ManufacturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manufacturer

    name = factory.Faker("name")
    country = factory.Faker("country")
    founded_year = factory.Faker("year")
    website = factory.Faker("url")
    logo = None


class AirplaneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Airplane

    name = factory.Faker("name")
    type = factory.SubFactory(AirplaneTypeFactory)
    manufacturer = factory.SubFactory(ManufacturerFactory)
    rows = factory.Faker("pyint", min_value=1, max_value=20)
    seats_in_row = factory.Faker("pyint", min_value=1, max_value=10)
    pilots_capacity = factory.Faker("pyint", min_value=1, max_value=MAX_PILOT_CAPACITY)
    personal_capacity = factory.Faker("pyint", min_value=0, max_value=6)
    year_of_manufacture = factory.Faker("year")
    fuel_capacity_l = factory.Faker("pyint", min_value=1000, max_value=10000)
    cargo_capacity_kg = factory.Faker("pyint", min_value=1000, max_value=10000)
    max_speed_kmh = factory.Faker("pyint", min_value=100, max_value=1000)
    max_distance_km = factory.Faker("pyint", min_value=1000, max_value=10000)
    image = None


class CrewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Crew

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    crew_type = factory.Iterator([CrewTypeChoices.FLIGHT_CREW, CrewTypeChoices.CABIN_CREW])

    @factory.lazy_attribute
    def position(self):
        if self.crew_type == CrewTypeChoices.FLIGHT_CREW:
            return random.choice(FlightCrewPositionChoices.values)

        return random.choice(CabinCrewPositionChoices.values)


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flight

    route = factory.SubFactory(RouteFactory)
    airplane = factory.SubFactory(AirplaneFactory)
    departure_time = factory.Faker("date_time")
    arrival_time = factory.Faker("date_time")

    @factory.post_generation
    def crew(self, create, extracted, **kwargs):
        if not create or extracted is not None:
            return

        for index in range(self.airplane.pilots_capacity):
            flight_crew = CrewFactory(
                first_name=f"FlightCrew first name {index + 1}",
                last_name=f"FlightCrew last name {index + 1}",
                crew_type=CrewTypeChoices.FLIGHT_CREW
            )

            self.crew.add(flight_crew)

        for index in range(self.airplane.personal_capacity):
            cabin_crew = CrewFactory(
                first_name=f"CabinCrew first name {index + 1}",
                last_name=f"CabinCrew last name {index + 1}",
                crew_type=CrewTypeChoices.CABIN_CREW
            )

            self.crew.add(cabin_crew)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date_time")

def generate_seat_and_row(flight: FlightFactory):
    airplane = flight.airplane

    while True:
        row = random.choice(range(1, airplane.rows + 1))
        seat = random.choice(range(1, airplane.seats_in_row + 1))

        tickets = Ticket.objects.filter(flight=flight, row=row, seat=seat)

        if not tickets.exists():
            return row, seat

class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    flight = factory.SubFactory(FlightFactory)
    order = factory.SubFactory(OrderFactory)
    booked_at = factory.Faker("date_time")

    @factory.lazy_attribute
    def row(self):
        row, seat = generate_seat_and_row(self.flight)
        self.__dict__["_generated_seat"] = seat
        return row

    @factory.lazy_attribute
    def seat(self):
        return self.__dict__.get("_generated_seat")
