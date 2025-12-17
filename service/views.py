from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import mixins

from service.models import Airport, Route, Manufacturer, Airplane
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
)

from .utils import params_from_query, params_from_query_integers


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

    def get_queryset(self):
        query = Airport.objects

        cities_query = self.request.query_params.get("city", None)
        years_query = self.request.query_params.get("year", None)

        if cities_query:
            q = Q()
            cities_param = params_from_query(cities_query)

            for city in cities_param:
                q |= Q(city__icontains=city)

            query = query.filter(q)

        if years_query:
            years_param = params_from_query_integers(years_query)
            query = query.filter(open_year__in=years_param)

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
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return ManufacturerListSerializer
            case 'retrieve' | 'update' | 'partial_update':
                return ManufacturerRetrieveSerializer
            case 'create':
                return ManufacturerCreateSerializer

        return ManufacturerSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    model = Airport

    def get_queryset(self):
        return Airplane.objects.select_related('manufacturer', 'type')

    def get_serializer_class(self):
        match self.action:
            case "list":
                return AirplaneListSerializer
            case "retrieve":
                return AirplaneRetrieveSerializer
            case "create":
                return AirplaneCreateSerializer
        return AirplaneSerializer
