from rest_framework import serializers

from service.models import Airport, Route, Manufacturer, Airplane


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


# Manufacturer
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "name", "country", "founded_year", "website", "logo")
        read_only_fields = ("id",)


class ManufacturerListSerializer(ManufacturerSerializer):
    airplanes_count = serializers.IntegerField(source="airplanes.count")

    class Meta:
        model = Manufacturer
        fields = ManufacturerSerializer.Meta.fields + ("airplanes_count",)


class ManufacturerAirplaneSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return f"{obj.type.name} ({obj.type.code})"

    class Meta:
        model = Airplane
        fields = ("id", "name", "type", "pilots_capacity", "passenger_seats_total", "personal_capacity", "year_of_manufacture", "image")


class ManufacturerRetrieveSerializer(ManufacturerSerializer):
    airplanes = ManufacturerAirplaneSerializer(many=True, read_only=True)

    class Meta(ManufacturerSerializer.Meta):
        fields = ManufacturerSerializer.Meta.fields + ("created_at", "updated_at", "airplanes")
        read_only_fields = ManufacturerSerializer.Meta.read_only_fields + ("created_at", "updated_at", "airplanes")


class ManufacturerCreateSerializer(ManufacturerSerializer):
    def to_representation(self, instance):
        return ManufacturerRetrieveSerializer(instance).data

# Airplane
class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "type",
            "manufacturer",
            "rows",
            "seats_in_row",
            "pilots_capacity",
            "personal_capacity",
            "year_of_manufacture",
            "fuel_capacity_l",
            "cargo_capacity_kg",
            "max_speed_kmh",
            "max_distance_km",
            "image",
        )


class AirplaneListSerializer(AirplaneSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type = serializers.SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return f"{obj.type.name} ({obj.type.code})"

    class Meta(AirplaneSerializer.Meta):
        fields = (
            "id",
            "name",
            "type",
            "manufacturer",
            "crew_capacity",
            "seats_total",
            "pilots_capacity",
            "year_of_manufacture",
            "fuel_capacity_l",
            "cargo_capacity_kg",
            "max_speed_kmh",
            "max_distance_km",
            "image",
        )


class AirplaneRetrieveSerializer(AirplaneSerializer):
    manufacturer = ManufacturerSerializer()
    type = serializers.SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return f"{obj.type.name} ({obj.type.code})"

    class Meta(AirplaneSerializer.Meta):
        fields = AirplaneListSerializer.Meta.fields + ("passenger_seats_total", )


class AirplaneCreateSerializer(AirplaneSerializer):
    def to_representation(self, instance):
        return AirplaneRetrieveSerializer(instance).data
