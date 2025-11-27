from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def get_test_image() -> SimpleUploadedFile:
    img = Image.new('RGB', (1, 1), color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return SimpleUploadedFile("test.png", buf.read(), content_type="image/png")
