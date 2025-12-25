from django.db.models import Q
from django_filters import FilterSet
from django_filters import filters

from .models import Airplane
from .utils import params_from_query


class AirportFilterSet(FilterSet):
    city = filters.CharFilter(method="get_city")
    year = filters.BaseInFilter(
        field_name='open_year',
        lookup_expr='in'
    )

    @staticmethod
    def get_city(queryset, _name, value):
        q = Q()
        cities_param = params_from_query(value)

        for city in cities_param:
            q |= Q(city__icontains=city)

        return queryset.filter(q)


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
