import pytest
from django.core.exceptions import ValidationError

from ..factories import CrewFactory
from ...choices import CabinCrewPositionChoices, FlightCrewPositionChoices, CrewTypeChoices


@pytest.mark.django_db
class TestCrewModel:
    def test_crew_should_validate_position_for_flight_crew_type(self):
        crew = CrewFactory(
            crew_type=CrewTypeChoices.FLIGHT_CREW,
            position=CabinCrewPositionChoices.FLIGHT_ATTENDANT
        )

        with pytest.raises(ValidationError) as exception:
            crew.full_clean()

        errors = exception.value.message_dict

        assert "Invalid Flight Attendant position for flight crew." in errors["__all__"]


    def test_crew_should_validate_position_for_cabin_crew_type(self):
        crew = CrewFactory(
            crew_type=CrewTypeChoices.CABIN_CREW,
            position=FlightCrewPositionChoices.CAPTAIN
        )

        with pytest.raises(ValidationError) as exception:
            crew.full_clean()

        errors = exception.value.message_dict

        assert "Invalid Captain position for cabin crew." in errors["__all__"]


    def test_crew_should_not_be_created_with_invalid_position(self):
        position_value = "Pilot"
        crew = CrewFactory(
            position=position_value
        )

        with pytest.raises(ValidationError) as exception:
            crew.full_clean()

        errors = exception.value.message_dict

        assert f"Value '{position_value}' is not a valid choice." in errors["position"]


    def test_crew_should_not_be_created_with_invalid_crew_type(self):
        crew_type_value = "Crew"
        crew = CrewFactory(
            crew_type=crew_type_value
        )

        with pytest.raises(ValidationError) as exception:
            crew.full_clean()

        errors = exception.value.message_dict

        assert f"Value '{crew_type_value}' is not a valid choice." in errors["crew_type"]



    def test_crew_model_should_be_created(self):
        crew = CrewFactory(
            first_name="John",
            last_name="Doe",
            crew_type=CrewTypeChoices.FLIGHT_CREW,
            position=FlightCrewPositionChoices.CAPTAIN,
        )

        assert crew.first_name == "John"
        assert crew.last_name == "Doe"
        assert crew.crew_type == CrewTypeChoices.FLIGHT_CREW
        assert crew.position == FlightCrewPositionChoices.CAPTAIN
