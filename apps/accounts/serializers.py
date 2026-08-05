from datetime import datetime

from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account
from .services import AuthService
from .validators import AccountUniqueValidator


class SessionSerializer(Serializer):
    sid = CharField(
        min_length=32,
        max_length=32,
        help_text="32-character hex session ID (UUID4 without dashes)",
    )


class TokensSerializer(Serializer):
    refresh = CharField(help_text="JWT refresh token")
    access = CharField(help_text="JWT access token")
    session = SessionSerializer()


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "username", "email", "password"
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True}
        }

    def create(self, validated_data: dict) -> Account:
        account = Account.objects.create_user(  # type:ignore
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        account.save()

        return account

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in "username", "email":
            validators = self.fields[field].validators

            for i, validator in enumerate(validators):
                if isinstance(validator, UniqueValidator):
                    validators[i] = AccountUniqueValidator(
                        queryset=validator.queryset,
                        message=validator.message
                    )
                    break


class AccountVerifyEmailSerializer(Serializer):
    token = CharField(
        allow_blank=False,
        trim_whitespace=True,
        max_length=512,
        write_only=True
    )
    email = EmailField(read_only=True)


class AccountLoginSerializer(Serializer):
    username = CharField(write_only=True)
    password = CharField(write_only=True)
    tokens = TokensSerializer(read_only=True)

    def validate(self, attrs: dict[str, str | Account]) -> dict[str, str | Account]:
        request: Request = self.context["request"]

        account: Account | None = authenticate(
            request=request._request,
            username=attrs["username"],
            password=attrs["password"]
        )  # type:ignore

        if account is None:
            raise AuthenticationFailed(detail="Invalid credentials")

        attrs["user"] = account

        return attrs


class AccountLogoutSerializer(Serializer):
    refresh_token = CharField()


class AccountTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data: dict[str, str] = super().validate(attrs)

        refresh: RefreshToken = self.token_class(attrs["refresh"])
        sid: str | None = refresh["sid"]
        if not sid or not AuthService.is_valid(sid=sid):
            raise AuthenticationFailed("Session not found or expired.")

        return data


class AccountChangePasswordSerializer(Serializer):
    old_password = CharField(write_only=True)
    new_password = CharField(write_only=True)
    refresh_token = CharField(write_only=True)
    tokens = TokensSerializer(read_only=True)


class AccountForgotPasswordSerializer(Serializer):
    email = EmailField()


class AccountForgotPasswordVerifySerializer(Serializer):
    email = EmailField()
    otp_code = CharField(write_only=True, min_length=6, max_length=6)
    reset_token = CharField(read_only=True)


class AccountResetPasswordSerializer(Serializer):
    token = CharField(write_only=True)
    password = CharField(write_only=True)
    tokens = TokensSerializer(read_only=True)
