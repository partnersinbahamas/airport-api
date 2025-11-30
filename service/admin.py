from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Airport, Route

admin.site.register(Route)

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
