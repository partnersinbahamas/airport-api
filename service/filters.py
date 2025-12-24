from django_filters import FilterSet
from django_filters import filters

from .models import Airplane

class AirplaneFilterSet(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    year = filters.BaseInFilter(
        field_name='year_of_manufacture',
        lookup_expr='in'
    )
    manufacturer = filters.CharFilter(
        field_name="manufacturer__name",
        lookup_expr="icontains"
    )
    type = filters.CharFilter(field_name="type__name", lookup_expr="icontains")

    class Meta:
        model = Airplane
        fields = (
            "year",
            "name",
            "manufacturer",
            "type",
            "fuel_capacity_l",
        )
