from django.db.models import Prefetch
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import mixins

from service.models import Airport, Route, Manufacturer, Airplane, Flight
from service.serializers import (
    AirportSerializer,
    AirportImageSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    ManufacturerSerializer,
    ManufacturerListSerializer,
    ManufacturerRetrieveSerializer,
    ManufacturerCreateSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    AirplaneCreateSerializer,
    FlightSerializer,
    FlightReadSerializer,
)
from .filters import AirplaneFilterSet, AirportFilterSet


@extend_schema_view(
    list=extend_schema(
        summary="Airports list",
        description="Get a list of airports filtered by city and year.",
        tags=["Airports"],
        request=None,
        parameters=[
            OpenApiParameter(
                name="year",
                type={"type": "array", "items": {"type": "number"}},
                required=False,
                description="Filter by year of opening.",
                examples=[
                    OpenApiExample(
                        name="None",
                        value=None,
                        summary="None",
                    ),
                    OpenApiExample(
                        name="2020",
                        value=[2020],
                        summary="2020",
                    ),
                    OpenApiExample(
                        name="2020, 1931",
                        value=[2020, 1931],
                        summary="2020, 1931",
                    ),
                ]
            ),
            OpenApiParameter(
                name="city",
                type={"type": "array", "items": {"type": "string"}},
                required=False,
                description="Filter by city name.",
                examples=[
                    OpenApiExample(
                        name="None",
                        value=None,
                        summary="None",
                    ),
                    OpenApiExample(
                        name="Berlin",
                        value=["Berlin"],
                        summary="Berlin",
                    ),
                    OpenApiExample(
                        name="Berlin, London",
                        value=["Berlin", "London"],
                        summary="Berlin, London",
                    ),
                ]
            ),
        ],
    ),
    create=extend_schema(
        summary="Create airport",
        description="Create a new airport.",
        tags=["Airports"],
        request=None,
    ),
    retrieve=extend_schema(
        summary="Airport details",
        description="Get details of an airport.",
        tags=["Airports"],
        request=None,
    ),
    update=extend_schema(
        summary="Update airport",
        description="Update an existing airport.",
        tags=["Airports"],
        request=AirportSerializer,
    ),
    partial_update = extend_schema(
        summary="Partial update airport",
        description="Partial update an existing airport.",
        tags=["Airports"],
        request=AirportSerializer,
    ),
    destroy=extend_schema(
        summary="Delete airport",
        description="Delete an airport.",
        tags=["Airports"],
        request=None
    )
)
class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    filterset_class = AirportFilterSet

    def get_queryset(self):
        query = Airport.objects


        return query

    @extend_schema(
        summary="Upload image",
        description="Upload an image to an airport.",
        tags=["Airports"],
        request=None,
    )
    @action(
        methods=['POST'],
        url_path="upload-image",
        detail=True,
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk:None):
        airport = self.get_object()

        serializer = self.get_serializer(airport, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return AirportImageSerializer

        return AirportSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Routes list",
        description="Get a list of routes.",
        tags=["Routes"],
        request=None,
    ),
    retrieve=extend_schema(
        summary="Route details",
        description="Get details of a route.",
        tags=["Routes"],
        request=None,
    ),
    create=extend_schema(
        summary="Create route",
        description="Create a new route.",
        tags=["Routes"],
        request=RouteSerializer,
        responses={201: RouteRetrieveSerializer},
    ),
    update=extend_schema(
        summary="Update route",
        description="Update an existing route.",
        tags=["Routes"],
        request=RouteSerializer,
    ),
    partial_update = extend_schema(
        summary="Partial update route",
        description="Partial update an existing route.",
        tags=["Routes"],
        request=RouteSerializer,
    ),
    destroy=extend_schema(
        summary="Delete route",
        description="Delete an existing route.",
        tags=["Routes"],
        request=None
    )
)
class RouteViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer

        if self.action == 'retrieve':
            return RouteRetrieveSerializer

        return RouteSerializer

    def get_queryset(self):
         return Route.objects.select_related('source', 'destination')


@extend_schema_view(
    desctiptopn="This viewset has no destroy possibility.",
    list=extend_schema(
        summary="Manufacturers list",
        description="Get a list of manufacturers.",
        tags=["Manufacturers"],
        request=None,
    ),
    create=extend_schema(
        summary="Create manufacturer",
        description="Create a new manufacturer.",
        tags=["Manufacturers"],
        request=ManufacturerSerializer,
        responses={201: ManufacturerRetrieveSerializer}
    ),
    retrieve=extend_schema(
        summary="Manufacturer details",
        tags=["Manufacturers"],
        description="Get details of a manufacturer.",
        request=None,
    ),
    update=extend_schema(
        summary="Update manufacturer",
        description="Update an existing manufacturer.",
        tags=["Manufacturers"],
        request=ManufacturerSerializer,
        responses={200: ManufacturerRetrieveSerializer}
    ),
    partial_update = extend_schema(
        summary="Partial update manufacturer",
        description="Partial update an existing manufacturer.",
        tags=["Manufacturers"],
        request=ManufacturerSerializer,
        responses={200: ManufacturerRetrieveSerializer}
    )
)
class ManufacturerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Manufacturer.objects.all().prefetch_related(
        Prefetch(
            'airplanes',
            queryset=Airplane.objects.select_related('type')
        )
    )

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return ManufacturerListSerializer
            case 'retrieve' | 'update' | 'partial_update':
                return ManufacturerRetrieveSerializer
            case 'create':
                return ManufacturerCreateSerializer

        return ManufacturerSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Airplanes list",
        description = "Get a list of airplanes.",
        tags=["Airplanes"],
        request=None,
        parameters=[
            OpenApiParameter(
                name="manufacturer",
                type=OpenApiTypes.STR,
                description="Filter by manufacturer name.",
                required=False,
                examples=[
                    OpenApiExample(
                        name="None",
                        value=None,
                        summary="None",
                    ),
                    OpenApiExample(
                        name="Boeing",
                        value="Boeing",
                        summary="Boeing",
                    ),
                    OpenApiExample(
                        name="Lockheed Martin",
                        value="Lockheed Martin",
                        summary="Lockheed Martin",
                    )
                ]
            ),
            OpenApiParameter(
                name="type",
                type=OpenApiTypes.STR,
                description="Filter by airplane type.",
                required=False,
                examples=[
                    OpenApiExample(
                        name="None",
                        value=None,
                        summary="None",
                    ),
                    OpenApiExample(
                        name="Commercial",
                        value="Commercial",
                        summary="Commercial",
                    ),
                    OpenApiExample(
                        name="Cargo",
                        value="Cargo",
                        summary="Cargo",
                    ),
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Airplane details",
        description="Get details of an airplane.",
        tags=["Airplanes"],
        request=None,
    ),
    create=extend_schema(
        summary="Create airplane",
        description="Create a new airplane.",
        tags=["Airplanes"],
        request=AirplaneSerializer,
        responses={201: AirplaneRetrieveSerializer}
    ),
    update=extend_schema(
        summary="Update airplane",
        description="Update an existing airplane.",
        tags=["Airplanes"],
        request=AirplaneSerializer,
        responses={200: AirplaneRetrieveSerializer}
    ),
    partial_update=extend_schema(
        summary="Partial update airplane",
        description="Partial update an existing airplane.",
        tags=["Airplanes"],
        request=AirplaneSerializer,
        responses={200: AirplaneRetrieveSerializer}
    ),
    destroy=extend_schema(
        summary="Delete airplane",
        description="Delete an existing airplane.",
        tags=["Airplanes"],
        request=None,
    )
)
class AirplaneViewSet(viewsets.ModelViewSet):
    model = Airplane
    filterset_class = AirplaneFilterSet

    def get_queryset(self):
        return (
            Airplane.objects
                .select_related('manufacturer', 'type')
                .prefetch_related(Prefetch(
                    'flights',
                    queryset=Flight.objects.prefetch_related("route__source", "route__destination"))
                )
        )

    def get_serializer_class(self):
        match self.action:
            case "list":
                return AirplaneListSerializer
            case "retrieve":
                return AirplaneRetrieveSerializer
            case "create" | "update" | "partial_update":
                return AirplaneCreateSerializer
        return AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    model = Flight

    def get_serializer_class(self):
        match self.action:
            case "list" | "retrieve":
                return FlightReadSerializer
        return FlightSerializer

    def get_queryset(self):
        return (
            Flight.objects
                .select_related(
                    "airplane",
                    "route__source",
                    "route__destination"
                )
                .prefetch_related("crew")
            )
