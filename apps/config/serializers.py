from rest_framework.serializers import CharField, Serializer


class StandardizedErrorItemSerializer(Serializer):
    code = CharField()
    detail = CharField()
    attr = CharField(allow_null=True)


class StandardizedErrorResponseSerializer(Serializer):
    type = CharField()
    errors = StandardizedErrorItemSerializer(many=True)
