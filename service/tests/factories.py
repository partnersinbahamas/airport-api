import factory
from django.contrib.auth import get_user_model

from ..constants import MAX_PILOT_CAPACITY
from ..models import Airport, Route, AirplaneType, Manufacturer, Airplane
from ..utils import generate_unique_letters_code


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
