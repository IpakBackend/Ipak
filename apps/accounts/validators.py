from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import Field
from rest_framework.validators import UniqueValidator


class AccountUniqueValidator(UniqueValidator):
    verification_timeout = timedelta(minutes=5)

    def __call__(self, value, serializer_field: Field):
        queryset: QuerySet = self.queryset.filter(
            **{serializer_field.source_attrs[-1]: value}
        )

        instance = getattr(serializer_field.parent, "instance", None)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)

        account = queryset.first()

        if account is None:
            return

        if account.email_verified:
            raise serializers.ValidationError(self.message)

        if account.created_at >= timezone.now() - self.verification_timeout:
            raise serializers.ValidationError(
                "This account is awaiting email verification."
            )

        account.delete()
