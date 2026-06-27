from config.validators import username_validators
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    UserManager,
)
from django.db.models import BigAutoField, BooleanField, CharField, EmailField, Manager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AccountManager(Manager):
    def create_user(self, username: str, email: str, password: str | None = None, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")

        email = BaseUserManager.normalize_email(email=email)

        account: Account = self.model(
            username=username, email=email, **extra_fields
        )
        account.set_password(raw_password=password)
        account.save(using=self._db)

        return account

    def get_by_natural_key(self, username: str):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_superuser(self, username: str, email: str, password: str | None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, password=password, **extra_fields)

    create_superuser.alters_data = True


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
    is_staff = BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = "id",
