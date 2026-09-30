from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    IntegerField,
    JSONField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from .models import Color, Product, ProductImage, Shop


class ColorSerializer(ModelSerializer):
    name = SerializerMethodField(method_name="get_name")

    class Meta:
        model = Color
        fields = "id", "name", "hex_value"
        read_only_fields = "id",

    def get_name(self, obj: Color) -> str:
        return str(obj)


class ShopSerializer(ModelSerializer):
    location = JSONField()

    class Meta:
        model = Shop
        fields = "id", "name", "description", \
            "address", "phone_number", "contact_information", \
            "opening_hours", "location", "owner"
        read_only_fields = "id", "owner"

    def perform_create(self, serializer):
        serializer.save(owner=self.context["request"].user)


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "id", "image", "position"
        read_only_fields = "id", "position"


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "id", "name", "gender", "material", "category", \
            "description", "brand", "manufacturer_country", \
            "size_system", "sizes", "colors", "shop", "is_available", "images"
        read_only_fields = "id", "shop", "images"


class ProductImageOrderSerializer(Serializer):
    images = ListField(child=IntegerField(min_value=1), min_length=1)

    def validate_images(self, value):
        product: Product = self.context["product"]

        if len(value) != product.images.count():
            raise ValidationError(
                "All product images must be included."
            )

        if len(value) != len(set(value)):
            raise ValidationError(
                "Image IDs must be unique."
            )

        actual_ids = set(
            product.images.values_list("id", flat=True)
        )

        if set(value) != actual_ids:
            raise ValidationError(
                "Invalid image IDs."
            )

        return value
