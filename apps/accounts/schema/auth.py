from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from ..backends import AccountJWTAuthenticationBackend


class AccountJWTScheme(SimpleJWTScheme):
    name = "AccountJWT"
    target_class = AccountJWTAuthenticationBackend
