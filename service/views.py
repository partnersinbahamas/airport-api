from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from service.models import Airport
from service.serializers import AirportSerializer, AirportImageSerializer


class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer

    def get_queryset(self):
        return Airport.objects.all()

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
