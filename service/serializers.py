from rest_framework import serializers

from service.models import Airport, Route, Manufacturer


# Airport
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "image", "open_year", "created_at")
        read_only_fields = ("id", "created_at")


class AirportImageSerializer(serializers.ModelSerializer):
    class Meta(AirportSerializer.Meta):
        fields = ("image", )


# Route
class RouteRetrieveSerializer(serializers.ModelSerializer):
    source = AirportSerializer()
    destination = AirportSerializer()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def to_representation(self, instance):
        return RouteRetrieveSerializer(instance).data


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(slug_field="name", read_only=True)
    destination = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta(RouteSerializer.Meta):
        fields = ("id", "source", "destination", "distance")


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "name", "country", "founded_year", "website", "logo")
        read_only_fields = ("id",)


class ManufacturerRetrieveSerializer(ManufacturerSerializer):
    class Meta(ManufacturerSerializer.Meta):
        fields = ManufacturerSerializer.Meta.fields + ("created_at", "updated_at")
        read_only_fields = ManufacturerSerializer.Meta.read_only_fields + ("created_at", "updated_at")


class ManufacturerCreateSerializer(ManufacturerSerializer):
    def to_representation(self, instance):
        return ManufacturerRetrieveSerializer(instance).data
