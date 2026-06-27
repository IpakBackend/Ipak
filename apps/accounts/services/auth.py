import time
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from django_redis import get_redis_connection
from ipware import get_client_ip
from redis.client import Pipeline, Redis
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

SESSION_TTL = 60 * 60 * 24 * 7


class AuthService:
    redis: Redis = get_redis_connection(alias="default")

    @classmethod
    def store_session(cls, sid: str, user: AbstractBaseUser, request: HttpRequest) -> None:
        ip: str = get_client_ip(request=request)[0] or ''

        data: dict[str, int | str] = {
            "user_id": user.pk,
            "device": request.META.get("HTTP_USER_AGENT", '')[:255],
            "ip": ip,
            "created_at": int(time.time()),
        }

        pipe: Pipeline = cls.redis.pipeline()
        pipe.hset(
            name=f"session:{sid}",
            mapping=data,
        )
        pipe.expire(name=f"session:{sid}", time=SESSION_TTL)

        user_sessions_key: str = f"user_sessions:{user.pk}"
        pipe.sadd(user_sessions_key, sid)

        pipe.execute()

    @classmethod
    def issue_tokens(cls, user: AbstractBaseUser, request: HttpRequest):
        sid: str = uuid.uuid4().hex

        refresh: RefreshToken = RefreshToken.for_user(user)
        refresh["sid"] = sid

        cls.store_session(sid=sid, user=user, request=request)

        return {
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "session": {"sid": sid}
        }

    @classmethod
    def get_session(cls, sid: str) -> dict[str, int | str] | dict:
        data: dict[bytes, bytes] = cls.redis.hgetall(
            name=f"session:{sid}")  # type:ignore

        return {key.decode(): value.decode() for key, value in data.items()}

    @classmethod
    def delete_session(cls, sid: str, user_id: int) -> None:
        pipe: Pipeline = cls.redis.pipeline()
        pipe.delete(f"session:{sid}")
        pipe.srem(f"user_sessions:{user_id}", sid)
        pipe.execute()

    @classmethod
    def is_valid(cls, sid: str) -> bool:
        return cls.redis.exists(f"session:{sid}")  # type:ignore

    @classmethod
    def invalidate_all_sessions(
        cls,
        user_id: int,
        exclude_sid: str | None = None
    ) -> None:
        key: str = f"user_sessions:{user_id}"
        sids: set[bytes] = cls.redis.smembers(key)  # type:ignore

        pipe: Pipeline = cls.redis.pipeline()

        for sid in sids:
            sid = sid.decode()

            if exclude_sid and sid == exclude_sid:
                continue

            pipe.delete(f"session:{sid}")
            pipe.srem(key, sid)

        pipe.execute()

    @classmethod
    def validate_refresh_token(cls, refresh_token: str, user_id: int, sid: str | None) -> RefreshToken:
        try:
            refresh = RefreshToken(refresh_token)  # type:ignore
        except Exception:
            raise ValidationError({
                "refresh_token": ["Invalid refresh token"]
            }, code="invalid")

        if str(refresh.get("user_id")) != str(user_id):
            raise ValidationError({
                "refresh_token": ["Token does not belong to this user"]
            }, code="invalid")

        if refresh.get("sid") != sid:
            raise ValidationError({
                "refresh_token": ["Token does not belong to this session"]
            }, code="invalid")

        return refresh
