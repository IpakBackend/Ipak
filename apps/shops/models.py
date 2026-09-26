from typing import Any

from colorfield.fields import ColorField
from config.validators import hexadecimal_validator
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    FloatField,
    ForeignKey,
    Manager,
    ManyToManyField,
    Model,
)
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

SIZE_SYSTEM_CHOICES = [
    ("alpha", "Alpha"),
    ("numeric", "Numeric")
]

ALPHA_SIZES = {"XXS", "XS", 'S', 'M', 'L', "XL", "XXL", "3XL", "4XL"}

# Create your models here.


class ColorManager(Manager):
    def create(self, **kwargs: Any) -> Any:
        if "name" in kwargs:
            kwargs["name"] = kwargs["name"].lower()

        if "hex_value" in kwargs:
            kwargs["hex_value"] = kwargs["hex_value"].capitalize()

        return super().create(**kwargs)


class Color(Model):
    name = CharField(max_length=24, unique=True)
    hex_value = ColorField(unique=True)
    # hex_value = CharField(
    #     max_length=6,
    #     unique=True,
    #     validators=[hexadecimal_validator]
    # )

    def __str__(self) -> str:
        return self.name.capitalize()

    class Meta:
        ordering = "id",


class Shop(Model):
    name = CharField(max_length=64)
    description = CharField(max_length=255)
    address = CharField(max_length=128)
    phone_number = PhoneNumberField()
    contact_information = CharField(max_length=64, blank=True)
    opening_hours = CharField(max_length=128)
    latitude = FloatField()
    longitude = FloatField()
    owner = ForeignKey(to="accounts.Account", on_delete=CASCADE)


class Product(Model):
    name = CharField(max_length=32)
    description = CharField(max_length=255)
    brand = CharField(max_length=32)
    manufacturer_country = CountryField(null=True)
    size_system = CharField(
        max_length=7,
        null=True,
        choices=SIZE_SYSTEM_CHOICES
    )
    sizes = ArrayField(
        base_field=CharField(max_length=8),
        null=True
    )
    colors = ManyToManyField(to=Color)
    shop = ForeignKey(to=Shop, on_delete=CASCADE)
    is_available = BooleanField(default=True)
