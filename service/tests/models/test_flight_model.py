import pytest

from service.choices import CrewTypeChoices
from ..factories import (
    FlightFactory,
    AirplaneFactory,
    RouteFactory,
    AirportFactory,
    AirplaneTypeFactory,
    CrewFactory
)


@pytest.mark.django_db
class TestFlightModel:
    def test_model_should_be_created(self):
        berlin_airport = AirportFactory(name="Airport Berlin", open_year=2000)
        paris_airport = AirportFactory(name="Airport Paris", open_year=2001)
        airplane_type = AirplaneTypeFactory(
            name="Airplane Type",
            code="AAA",
            purpose="Some airplane type purpose."
        )

        route = RouteFactory(
            source=berlin_airport,
            destination=paris_airport,
            distance=10
        )
        airplane = AirplaneFactory(
            name="Flight airplane",
            type=airplane_type,
            personal_capacity=2,
            pilots_capacity=2
        )

        cabin_crew_1 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)
        cabin_crew_2 = CrewFactory(crew_type=CrewTypeChoices.CABIN_CREW)

        flight_crew_1 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)
        flight_crew_2 = CrewFactory(crew_type=CrewTypeChoices.FLIGHT_CREW)

        flight = FlightFactory(
            route=route,
            airplane=airplane,
            departure_time="2022-01-01T12:00:00Z",
            arrival_time="2022-01-01T12:30:00Z",
            crew=[]
        )

        flight.crew.set([cabin_crew_1, cabin_crew_2, flight_crew_1, flight_crew_2])

        assert flight.departure_time == "2022-01-01T12:00:00Z"
        assert flight.arrival_time == "2022-01-01T12:30:00Z"

        assert str(flight.route) == ("Airport Berlin (2000) -"
                                     " Airport Paris (2001) (10km.)")
        assert flight.airplane.name == "Flight airplane"

        assert flight_crew_1 in flight.crew.all()
        assert flight_crew_2 in flight.crew.all()

        assert cabin_crew_1 in flight.crew.all()
        assert cabin_crew_2 in flight.crew.all()

        assert str(flight) == ("Airport Berlin (2000) - Airport Paris (2001) (10km.) "
                               "- Flight airplane - AAA")

