from typing import Any

from colorfield.fields import ColorField
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Manager,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    UniqueConstraint,
)
from django.db.models.manager import Manager
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

SIZE_SYSTEM_CHOICES = [
    ("alpha", "Alpha"),
    ("numeric", "Numeric")
]

ALPHA_SIZES = {"XXS", "XS", 'S', 'M', 'L', "XL", "XXL", "3XL", "4XL"}

CATEGORY_CHOICES = [
    ("shoes", "Shoes"),
    ("tops", "Tops"),
    ("bottoms", "Bottoms"),
    ("dresses", "Dresses"),
    ("outerwear", "Outerwear"),
    ("underwear", "Underwear"),
    ("accessories", "Accessories"),
    ("others", "Others")
]

GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("unisex", "Unisex")
]

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
    location = PointField(geography=True, srid=4326)
    owner = ForeignKey(to="accounts.Account", on_delete=CASCADE)


class Product(Model):
    name = CharField(max_length=32)
    category = CharField(
        max_length=16,
        default="others",
        choices=CATEGORY_CHOICES
    )
    material = CharField(max_length=32, blank=True)
    gender = CharField(max_length=6, choices=GENDER_CHOICES, default="unisex")
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
    images: Manager["ProductImage"]


class ProductImage(Model):
    product = ForeignKey(to=Product, on_delete=CASCADE, related_name="images")
    image = ImageField(upload_to="products/")
    position = PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["product", "position"],
                name="unique_product_image_position"
            )
        ]
        ordering = "product", "-position"
