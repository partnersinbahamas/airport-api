from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Airport, Route, AirplaneType, Manufacturer, Airplane, Crew, Flight
from .utils import get_admin_url
from .forms import FlightForm

admin.site.register(Crew)

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "open_year", "render_image", "created_at")
    list_filter = ("open_year", "created_at")
    search_fields = ("name", "city")
    readonly_fields = ("render_image", "image")

    def render_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" height="80px">')
        return None

    render_image.short_description = "Picture"


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display_links = ("id", "source_link", "destination_link")
    list_display = ("id", "source_link", "destination_link", "distance")
    search_fields = ("source__name", "destination__name")
    list_filter = ("distance",)

    def source_link(self, obj):
        if obj.source:
            url = get_admin_url(obj.source)
            return format_html(mark_safe('<a href="{}">{}</a>'), url, obj.source.name)
        return None

    source_link.short_description = "Source"

    def destination_link(self, obj):
        if obj.destination:
            url = get_admin_url(obj.destination)
            return format_html(mark_safe('<a href="{}">{}</a>'), url, obj.destination.name)
        return None

    destination_link.short_description = "Destination"


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "purpose")
    search_fields = ("name", "code")


class AirplaneInline(admin.TabularInline):
    model = Airplane
    extra = 0


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    inlines = [AirplaneInline]
    list_display = ("id", "name", "country", "founded_year", "website", "render_logo", "created_at")
    search_fields = ("name", "country")
    readonly_fields = ("render_logo", "logo")

    def render_logo(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50px" height="50px">')
        return None

    render_logo.short_description = "Logotype"



@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "manufacturer", "year_of_manufacture", "passenger_seats_total", "crew_capacity", "pilots_capacity", "cargo_capacity_kg", "max_distance_km", "render_image")
    search_fields = ("name", "manufacturer__name")
    list_filter = ("year_of_manufacture", "pilots_capacity", "cargo_capacity_kg", "max_distance_km")
    readonly_fields = ("render_image", "image")

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields

        return self.readonly_fields + ("passenger_seats_total", "crew_capacity")


    def render_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="70px" height="50px">')
        return None

    render_image.short_description = "Picture"


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    form = FlightForm

    list_display = ("id", "route", "airplane", "departure_time", "arrival_time")
    list_filter = ("departure_time", "arrival_time")
    search_fields = ("route__source__name", "route__destination__name")