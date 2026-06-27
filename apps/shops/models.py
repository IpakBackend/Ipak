from django.db.models import (
    CASCADE,
    CharField,
    EmailField,
    FloatField,
    ForeignKey,
    Model,
    TextField,
)
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Shop(Model):
    name = CharField(max_length=255)
    description = TextField()
    address = CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = EmailField()
    opening_hours = CharField(max_length=255)
    latitude = FloatField()
    longitude = FloatField()
    owner = ForeignKey(to="accounts.Account", on_delete=CASCADE)
