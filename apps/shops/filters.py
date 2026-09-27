from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import QuerySet
from django_filters.rest_framework import FilterSet, NumberFilter

from .models import Product, Shop


class ProximityFilterSet(FilterSet):
    latitude = NumberFilter()
    longitude = NumberFilter()
    radius = NumberFilter()

    location_field: str

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        queryset = super().filter_queryset(queryset)

        latitude: float | None = self.form.cleaned_data.get("latitude")
        longitude: float | None = self.form.cleaned_data.get("longitude")
        radius: float | None = self.form.cleaned_data.get("radius")

        if latitude is None or longitude is None or radius is None:
            return queryset

        point = Point(x=longitude, y=latitude, srid=4326)

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
        fields = "name", "address", "latitude", "longitude", "radius"


class ProductFilter(ProximityFilterSet):
    location_field = "shop__location"

    class Meta:  # type:ignore
        model = Product
        fields = "name",  "category", "material", \
            "brand", "manufacturer_country", "colors", \
            "is_available", "latitude", "longitude", "radius"
