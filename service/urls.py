from django.urls import path, include
from rest_framework import routers

from service.views import AirportViewSet, RouteViewSet, ManufacturerViewSet

app_name = "service"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet, basename="airports")
router.register("routes", RouteViewSet, basename="routes")
router.register("manufacturers", ManufacturerViewSet, basename="manufacturers")

urlpatterns = [
    path("", include(router.urls))
]
