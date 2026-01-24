from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATIC_ROOT = "staticfiles/"

DEBUG_TOOLBAR_CONFIG = {}

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# S3/Cloudflare R2 backend
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.environ["R2_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["R2_SECRET_ACCESS_KEY"]

AWS_STORAGE_BUCKET_NAME = "airport-api-media"
AWS_S3_ENDPOINT_URL = "https://eb1e85778e75b9d483bc55441c421e99.r2.cloudflarestorage.com"
AWS_S3_CUSTOM_DOMAIN = "pub-5f383f056e5e48c6addfb69f3534a08e.r2.dev"

AWS_S3_REGION_NAME = "auto"

AWS_S3_ADDRESSING_STYLE = "path"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False

MEDIA_URL = "https://pub-5f383f056e5e48c6addfb69f3534a08e.r2.dev/"