from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Airport, Route, AirplaneType, Manufacturer
from .utils import get_admin_url


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


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "founded_year", "website", "render_logo", "created_at")
    search_fields = ("name", "country")
    readonly_fields = ("render_logo", "logo")

    def render_logo(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50px" height="50px">')
        return None

    render_logo.short_description = "Logotype"
