import pytest
from ..factories import AirplaneFactory, ManufacturerFactory, AirplaneTypeFactory
from ...models import Airplane


@pytest.mark.django_db
class TestAirplaneModel:
    def test_airplane_should_be_with_rows_and_seats_in_row_created(self):
        manufacturer = ManufacturerFactory(name="Manufacturer")
        airplane_type = AirplaneTypeFactory(name="Airplane A380", code="AA1")

        airplane = AirplaneFactory(
            name="Airplane A380",
            rows=16,
            seats_in_row=6,
            type=airplane_type,
            manufacturer=manufacturer,
            pilots_capacity=2,
            personal_capacity=4,
            year_of_manufacture=2020,
            fuel_capacity_l=10000,
            cargo_capacity_kg=10000,
            max_speed_kmh=100,
            max_distance_km=10000,
            image="image.png"
        )


        assert airplane.name == "Airplane A380"
        assert airplane.rows == 16
        assert airplane.seats_in_row == 6
        assert airplane.type.name == airplane_type.name
        assert airplane.manufacturer.name == manufacturer.name
        assert airplane.pilots_capacity == 2

        assert airplane.personal_capacity == 4
        assert airplane.year_of_manufacture == 2020
        assert airplane.fuel_capacity_l == 10000
        assert airplane.cargo_capacity_kg == 10000
        assert airplane.max_speed_kmh == 100
        assert airplane.max_distance_km == 10000
        assert airplane.image == "image.png"

        # properties
        crew_capacity = 2 + 4
        passenger_seats_total = 16 * 6

        assert airplane.crew_capacity == crew_capacity
        assert airplane.passenger_seats_total == passenger_seats_total
        assert airplane.seats_total == passenger_seats_total + crew_capacity

    def test_airplane_should_be_without_created(self):
        manufacturer = ManufacturerFactory(name="Manufacturer")
        airplane_type = AirplaneTypeFactory(name="Airplane A380", code="AA1")

        airplane = AirplaneFactory(
            name="Airplane A380",
            rows=None,
            seats_in_row=None,
            type=airplane_type,
            manufacturer=manufacturer,
            pilots_capacity=1,
            personal_capacity=2,
            year_of_manufacture=2020,
            fuel_capacity_l=10000,
            cargo_capacity_kg=10000,
            max_speed_kmh=100,
            max_distance_km=10000,
            image="image.png"
        )

        assert airplane.name == "Airplane A380"
        assert airplane.rows == None
        assert airplane.seats_in_row == None
        assert airplane.type.name == airplane_type.name
        assert airplane.manufacturer.name == manufacturer.name
        assert airplane.pilots_capacity == 1

        assert airplane.personal_capacity == 2
        assert airplane.year_of_manufacture == 2020
        assert airplane.fuel_capacity_l == 10000
        assert airplane.cargo_capacity_kg == 10000
        assert airplane.max_speed_kmh == 100
        assert airplane.max_distance_km == 10000
        assert airplane.image == "image.png"

        # properties
        crew_capacity = 1 + 2
        passenger_seats_total = 0

        assert airplane.crew_capacity == crew_capacity
        assert airplane.passenger_seats_total == passenger_seats_total
        assert airplane.seats_total == passenger_seats_total + crew_capacity
