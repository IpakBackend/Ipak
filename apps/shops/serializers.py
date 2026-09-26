from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Color, Shop


class ColorSerializer(ModelSerializer):
    name = SerializerMethodField(method_name="get_name")

    class Meta:
        model = Color
        fields = "id", "name", "hex_value"
        read_only_fields = "id",

    def get_name(self, obj: Color) -> str:
        return str(obj)


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = "id", "name", "description", \
            "address", "phone_number", "contact_information", \
            "opening_hours", "latitude", "longitude", "owner"
        read_only_fields = "id", "owner"

    def perform_create(self, serializer):
        serializer.save(owner=self.context["request"].user)
