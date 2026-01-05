from django.urls import path, include
from rest_framework import routers

from service.views import AirportViewSet, RouteViewSet, ManufacturerViewSet, AirplaneViewSet, FlightViewSet, OrdersViewSet

app_name = "service"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet, basename="airports")
router.register("routes", RouteViewSet, basename="routes")
router.register("manufacturers", ManufacturerViewSet, basename="manufacturers")
router.register("airplanes", AirplaneViewSet, basename="airplanes")
router.register("flights", FlightViewSet, basename="flights")
router.register("orders", OrdersViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls))
]
