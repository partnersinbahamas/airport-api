from rest_framework import serializers

from service.models import Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "image", "open_year", "created_at")
        read_only_fields = ("id", "created_at")


class AirportImageSerializer(serializers.ModelSerializer):
    class Meta(AirportSerializer.Meta):
        fields = ("image", )
