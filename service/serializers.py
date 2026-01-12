from django.db import transaction
from rest_framework import serializers

from service.choices import CrewTypeChoices
from service.models import Airport, Route, Manufacturer, Airplane, Crew, Flight, Order, Ticket


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

    def validate(self, data):
        if data["source"] == data["destination"]:
            raise serializers.ValidationError({"detail": "Source and destination cannot be the same."})

        return data


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
    flights = serializers.IntegerField(source="flights.count")

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
            "flights",
            "image",
        )


class AirplaneFlightsSerializer(serializers.ModelSerializer):
    route = RouteRetrieveSerializer(read_only=True)
    class Meta:
        model = Flight
        fields = ("id", "route", "departure_time", "arrival_time")


class AirplaneRetrieveSerializer(AirplaneSerializer):
    manufacturer = ManufacturerSerializer()
    type = serializers.SerializerMethodField()
    flights = AirplaneFlightsSerializer(many=True, read_only=True)

    @staticmethod
    def get_type(obj):
        return f"{obj.type.name} ({obj.type.code})"

    class Meta(AirplaneSerializer.Meta):
        fields = AirplaneListSerializer.Meta.fields + ("passenger_seats_total", "flights", "rows", "seats_in_row")


# Flight
class FlightCrewSerializer(serializers.ModelSerializer):
    crew_type = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "crew_type", "position")

    @staticmethod
    def get_crew_type(obj):
        return obj.crew_type_label

    @staticmethod
    def get_position(obj):
        return obj.position_label


class FlightAirplaneSerializer(serializers.ModelSerializer):
    passenger_seats = serializers.IntegerField(source="passenger_seats_total")
    manufacturer = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "manufacturer",
            "pilots_capacity",
            "personal_capacity",
            "passenger_seats",
            "image",
        )


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.select_related("source", "destination")
    )
    airplane = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.select_related("manufacturer", "type")
    )

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "crew", "departure_time", "arrival_time")

    def validate(self, data):
        crew = data.get("crew")
        airplane = data.get("airplane")

        if crew is not None and airplane is not None:
            flight_crew = [crew_person for crew_person in crew if crew_person.crew_type == CrewTypeChoices.FLIGHT_CREW]
            cabin_crew = [crew_person for crew_person in crew if crew_person.crew_type == CrewTypeChoices.CABIN_CREW]

            if len(cabin_crew) > airplane.personal_capacity:
                raise serializers.ValidationError({"detail": f"The number of cabin crew exceeds the airline's personal capacity."})

            if len(flight_crew) > airplane.pilots_capacity:
                raise serializers.ValidationError({"detail": f"The number of flight crew exceeds the airline's pilot capacity."})

            if len(cabin_crew) < airplane.personal_capacity:
                raise serializers.ValidationError({"detail": f"The number of airline personal capacity must be at least { airplane.personal_capacity}."})

            if len(flight_crew) < airplane.pilots_capacity:
                raise serializers.ValidationError({"detail": f"The number of airline pilots capacity must be at least {airplane.pilots_capacity}."})

        return data


class FlightReadSerializer(serializers.ModelSerializer):
    crew = FlightCrewSerializer(many=True, read_only=True)
    airplane = FlightAirplaneSerializer(read_only=True)
    route = RouteRetrieveSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "crew", "departure_time", "arrival_time")


class TicketFlightSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    airplane = serializers.SlugRelatedField(slug_field="name", read_only=True)

    @staticmethod
    def get_route(obj):
        return f"{obj.route.source.name} - {obj.route.destination.name}"

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, data):
        Ticket.validate_seat_number(
            row=data["row"],
            seat=data["seat"],
            airplane=data["flight"].airplane
        )
        return data


class TicketRetrieveSerializer(serializers.ModelSerializer):
    flight = TicketFlightSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "booked_at")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "user", "created_at", "tickets")
        read_only_fields = ("id", "user", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets = validated_data.pop("tickets")

            if tickets:
                order = Order.objects.create(**validated_data)

                for ticket in tickets:
                    Ticket.objects.create(order=order, **ticket)

                return order

            return None


class OrderReadSerializer(serializers.ModelSerializer):
    tickets = TicketRetrieveSerializer(many=True, allow_empty=True)

    class Meta:
        model = Order
        fields = ("id", "user", "tickets", "created_at")
