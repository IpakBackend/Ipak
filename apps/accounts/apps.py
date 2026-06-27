from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "Accounts"

    def ready(self) -> None:
        from .schema import auth
