from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from service.models import Airport
from service.serializers import AirportSerializer, AirportImageSerializer
from .utils import params_from_query, params_from_query_integers


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
