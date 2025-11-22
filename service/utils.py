import uuid
from pathlib import Path

from django.utils.text import slugify

def create_airport_image_url(airport: "Airport", filename: str) -> Path:
    path = f"{slugify(airport.name)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/airports/") / Path(path)
