import random
import string
from secrets import token_urlsafe

from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django_redis import get_redis_connection
from redis.client import Redis
from rest_framework.exceptions import Throttled, ValidationError


class OTPService:
    redis: Redis = get_redis_connection(alias="default")

    @classmethod
    def generate_otp(cls, email: str) -> str:
        otp_code: str = ''.join(random.choices(string.digits, k=6))
        otp_hash: str = make_password(password=otp_code)
        key: str = f"otp:{email}"

        created: bool = cls.redis.set(  # type:ignore
            name=key, value=otp_hash, ex=120, nx=True
        )

        if not created:
            ttl: int = cls.redis.ttl(name=key)  # type:ignore

            raise Throttled(
                wait=ttl,
                detail="You already have an existing OTP code. Please wait before generating a new one.",
                code="otp_rate_limited"
            )

        return otp_code

    @classmethod
    def delete_otp(cls, email: str) -> None:
        cls.redis.delete(f"otp:{email}")

    @staticmethod
    def send_otp_code(email: str, otp_code: str) -> None:
        subject: str = "OTP code"
        message:  str = "Your OTP code is: " + str(otp_code)

        email_message = EmailMessage(
            subject=subject,
            body=message,
            to=[email]

        )
        email_message.content_subtype = "html"
        email_message.send(fail_silently=False)

    @classmethod
    def check_otp(cls, email: str, otp_code: str) -> None:
        stored_hash: str = cls.redis.get(f"otp:{email}")  # type:ignore

        if not stored_hash or \
                not check_password(otp_code, stored_hash.decode()):  # type:ignore
            raise ValidationError(
                detail={"otp_code": ["Invalid OTP code"]}, code="invalid")

    @classmethod
    def generate_reset_token(cls, email: str) -> str:
        token: str = token_urlsafe(32)
        token_hash: str = make_password(password=token)
        key: str = f"reset_token:{token_hash}"

        created: bool = cls.redis.set(  # type:ignore
            name=key, value=email, ex=120, nx=True
        )

        if not created:
            ttl: int = cls.redis.ttl(name=key)  # type:ignore

            raise Throttled(
                wait=ttl,
                detail="You already have an existing reset token. Please wait before generating a new one.",
                code="reset_rate_limited"
            )

        return token

    @classmethod
    def get_email_by_reset_token(cls, token: str) -> bytes | None:
        return cls.redis.get(name=f"reset_token:{token}")  # type:ignore
