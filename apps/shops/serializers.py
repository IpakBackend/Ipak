from rest_framework.serializers import JSONField, ModelSerializer, SerializerMethodField

from .models import Color, Product, Shop


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


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "id", "name", "material", "category", \
            "description", "brand", "manufacturer_country", \
            "size_system", "sizes", "colors", "shop", "is_available"
        read_only_fields = "id", "shop"
