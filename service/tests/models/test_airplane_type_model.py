import pytest
from django.db import transaction, IntegrityError

from service.models import AirplaneType
from service.tests.factories import AirplaneTypeFactory


@pytest.mark.django_db
class TestAirplaneTypeModel:
    def test_airplane_type_model_should_be_created(self):
        airplane_type = AirplaneTypeFactory(
            name="Airplane Type",
            code="AAA",
            purpose="Some airplane type purpose."
        )

        assert airplane_type.name == "Airplane Type"
        assert airplane_type.code == "AAA"
        assert airplane_type.purpose == "Some airplane type purpose."


    def test_airplane_type_code_should_be_unique(self):
        AirplaneTypeFactory(
            name="Airplane Type",
            code="AAA",
            purpose="Some airplane type purpose."
        )

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                AirplaneTypeFactory(
                    name="Airplane Type 2",
                    code="AAA",
                    purpose="Some airplane type purpose 2."
                )

        assert AirplaneType.objects.count() == 1
