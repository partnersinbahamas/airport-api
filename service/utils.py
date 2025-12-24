import uuid
import string
from pathlib import Path

from django.urls import reverse
from django.utils.text import slugify

def create_airport_image_url(airport: "Airport", filename: str) -> Path:
    path = f"{slugify(airport.name)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/airports/") / Path(path)


def create_manufacturer_logo_url(manufacturer: "Manufacturer", filename: str) -> Path:
    path = f"{slugify(manufacturer.name)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/manufacturers/") / Path(path)


def create_airplane_image_url(airplane: "Airplane", filename: str) -> Path:
    path = f"{slugify(airplane.name)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/airplanes/") / Path(path)


def params_from_query(query: str | None) -> list:
    return [param.strip() for param in query.split(',')]


def params_from_query_integers(query: str | None) -> list:
    return [int(param.strip()) for param in query.split(',')]


def get_admin_url(obj):
    return reverse(
        f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
        args=[obj.pk]
    )


def generate_unique_letters_code(iterations: int = 3):
    letters = string.ascii_uppercase

    return (
        letters[(iterations // 26**2) % 26] +
        letters[(iterations // 26) % 26] +
        letters[iterations % 26]
    )
