from django.db import models


class CrewTypeChoices(models.TextChoices):
    FLIGHT_CREW = 'flight_crew', 'Flight crew'
    CABIN_CREW = 'cabin_crew', 'Cabin crew'


class FlightCrewPositionChoices(models.TextChoices):
    CAPTAIN = 'captain', 'Captain'
    CO_PILOT = 'co_pilot', 'Co-Pilot'
    FLIGHT_ENGINEER = 'flight_engineer', 'Flight Engineer'
    NAVIGATOR = 'navigator', 'Navigator'

class CabinCrewPositionChoices(models.TextChoices):
    FLIGHT_ATTENDANT = 'flight_attendant', 'Flight Attendant'
    SENIOR_FLIGHT_ATTENDANT = 'senior_flight_attendant', 'Senior Flight Attendant'
    SAFETY_OFFICER = 'safety_officer', 'Safety Officer'


CREW_POSITION_CHOICES_LIST = list(FlightCrewPositionChoices.choices) + list(CabinCrewPositionChoices.choices)
