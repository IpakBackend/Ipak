from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import Token

from .models import Account
from .services import AuthService


class AccountAuthenticationBackend(BaseBackend):
    def authenticate(
            self,
            request: HttpRequest,
            username: str | None = None,
            password: str | None = None,
            **kwargs
    ) -> Account | None:
        try:
            account: Account = Account.objects.get(username=username)
            if password is not None and account.check_password(raw_password=password):
                return account
        except Account.DoesNotExist:
            return None

        return None

    def get_user(self, user_id: int) -> Account | None:
        try:
            return Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return None


class AccountJWTAuthenticationBackend(JWTAuthentication):
    def authenticate(self, request: Request) -> tuple[Account, Token] | None:
        header: bytes | None = self.get_header(request=request)
        if header is None:
            return None

        raw_token: bytes | None = self.get_raw_token(header=header)
        if raw_token is None:
            return None

        validated_token: Token = self.get_validated_token(raw_token=raw_token)

        return self._authenticate_credentials(validated_token=validated_token)

    def _authenticate_credentials(
            self,
            validated_token: Token,
    ) -> tuple[Account, Token]:
        account: Account = self.get_user(validated_token=validated_token)

        sid: str | None = validated_token.payload.get("sid")
        if not sid:
            raise AuthenticationFailed("Missing or invalid session id")

        if not AuthService.is_valid(sid=sid):
            raise AuthenticationFailed("Session revoked")

        return account, validated_token


"""
{
    "tokens": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NzM3ODE4NSwiaWF0IjoxNzc2NTE0MTg1LCJqdGkiOiJiZWMyNGZmZjUyMTQ0ZDkwYTg5YjZlMzQwZDE1NWQ1YSIsInVzZXJfaWQiOiIxIiwic2lkIjoiZGRjMzY5NmRlYjE2NDYxMTllN2JkZDI5OWY4MTZkNWEifQ.xjbEe_fD4hcclIN_zcs2uhMmij4ImOG5txbPl2RxC6w",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2NTE3Nzg1LCJpYXQiOjE3NzY1MTQxODUsImp0aSI6IjhmOTYyMWVmOTUwMDQ2OGY4YjNiNDI1NjNjYmM4OWVmIiwidXNlcl9pZCI6IjEiLCJzaWQiOiJkZGMzNjk2ZGViMTY0NjExOWU3YmRkMjk5ZjgxNmQ1YSJ9.aFcHQd7GUTrkNYt8Q7weoFD2Z5PCgeutYuf77zaifvY"
    },
    "session": {
        "sid": "ddc3696deb1646119e7bdd299f816d5a"
    }
}

{
  "tokens": {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NzM4MDM2MSwiaWF0IjoxNzc2NTE2MzYxLCJqdGkiOiI4MDJiMTVmNTkwNWM0MWNkYmEwZjJjN2ZkMjVhNzcwYyIsInVzZXJfaWQiOiIxIiwic2lkIjoiZjNmNDczOTUzZmIzNGRiYjhlZjk4MzNlZDExM2IyNTcifQ.62bPRszPhm5SK4HPvxcGsZf9cJ3Gj5boG2J-FKID8oU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2NTE5OTYxLCJpYXQiOjE3NzY1MTYzNjEsImp0aSI6IjA2YTU4MjdjODdkNDRjNzM5NWY0ZTQyMTM5NjhhYjVmIiwidXNlcl9pZCI6IjEiLCJzaWQiOiJmM2Y0NzM5NTNmYjM0ZGJiOGVmOTgzM2VkMTEzYjI1NyJ9.En8s6Dt18_HkhmgEX8YRJeNYxBLjOhiEjwoFEnu6j8U"
  },
  "session": {
    "sid": "f3f473953fb34dbb8ef9833ed113b257"
  }
}
"""
