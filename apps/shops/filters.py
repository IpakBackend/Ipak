from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import QuerySet
from django_filters.rest_framework import CharFilter, FilterSet

from .models import Product, Shop


class ProximityFilterSet(FilterSet):
    proximity = CharFilter(method="filter_proximity")

    location_field: str

    def filter_proximity(
            self,
            queryset: QuerySet,
            name: str,
            value: str
    ) -> QuerySet:
        try:
            latitude, longitude, radius = map(float, value.split(","))
        except ValueError:
            return queryset

        point = Point(
            x=longitude,
            y=latitude,
            srid=4326,
        )

        return queryset.filter(
            **{
                f"{self.location_field}__distance_lte": (
                    point,
                    D(km=radius),
                )
            }
        )

    class Meta:
        abstract = True


class ShopFilter(ProximityFilterSet):
    location_field = "location"

    class Meta:  # type:ignore
        model = Shop
        fields = "name", "address"


class ProductFilter(ProximityFilterSet):
    location_field = "shop__location"

    class Meta:  # type:ignore
        model = Product
        fields = "name", "gender", "category", "material", "brand", \
            "manufacturer_country", "colors", "is_available"
