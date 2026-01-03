from django import forms
from django.core.exceptions import ValidationError

from .choices import CrewTypeChoices
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ("route", "airplane", "crew", "departure_time", "arrival_time")

    def clean(self):
        cleaned_data = super().clean()

        crew = cleaned_data.get("crew")
        airplane = cleaned_data.get("airplane")

        if crew is not None and airplane is not None:
            flight_crew = crew.filter(crew_type=CrewTypeChoices.FLIGHT_CREW)
            cabin_crew = crew.filter(crew_type=CrewTypeChoices.CABIN_CREW)

            if cabin_crew.count() > airplane.personal_capacity:
                raise ValidationError(f"The number of cabin crew exceeds the airline's personal capacity.")

            if flight_crew.count() > airplane.pilots_capacity:
                raise ValidationError(f"The number of flight crew exceeds the airline's pilot capacity.")

            if cabin_crew.count() < airplane.personal_capacity:
                raise ValidationError(f"The number of airline personal capacity must be at least {airplane.personal_capacity}.")

            if flight_crew.count() < airplane.pilots_capacity:
                raise ValidationError(f"The number of airline pilots capacity must be at least {airplane.pilots_capacity}.")

        return cleaned_data
