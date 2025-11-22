from django.urls import path, include
from rest_framework import routers

from service.views import AirportViewSet

app_name = "service"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet, basename="airports")

urlpatterns = [
    path("", include(router.urls))
]
