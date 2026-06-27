from typing import Literal

from config.validators import username_validators
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
    User,
    UserManager,
)
from django.db.models import BigAutoField, BooleanField, CharField, EmailField, Manager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AccountManager(Manager):
    def create_user(self, username: str, email: str, password: str | None = None):
        if not username:
            raise ValueError("The given username must be set")

        email = BaseUserManager.normalize_email(email=email)

        account: Account = self.model(username=username, email=email)
        account.set_password(raw_password=password)
        account.save(using=self._db)

        return account

    def get_by_natural_key(self, username: str):
        return self.get(**{self.model.USERNAME_FIELD: username})

    async def aget_by_natural_key(self, username: str):
        return await self.aget(**{self.model.USERNAME_FIELD: username})


class Account(AbstractBaseUser, PermissionsMixin):
    id: BigAutoField
    username = CharField(
        verbose_name=_("username"),
        max_length=16,
        unique=True,
        validators=username_validators
    )
    email = EmailField(
        verbose_name=_("email address"),
        unique=True
    )
    is_active = BooleanField(
        verbose_name=_("is active"),
        default=True,
    )

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = "id",
