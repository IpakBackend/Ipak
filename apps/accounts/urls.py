from django.urls import include, path

from .views import (
    AccountChangePasswordView,
    AccountForgotPasswordView,
    AccountLoginView,
    AccountLogoutView,
    AccountMeView,
    AccountSignupView,
    AccountTokenRefreshView,
    AccountForgotPasswordVerifyView,
    AccountResetPasswordView
)

urlpatterns = [
    path(
        "signup/",
        AccountSignupView.as_view(),
        name="api_account_signup"
    ),
    path("login/", AccountLoginView.as_view(), name="api_account_login"),
    path(
        "logout/",
        AccountLogoutView.as_view(),
        name="api_account_logout"
    ),
    path("me/", AccountMeView.as_view(), name="api_account_me"),
    path(
        "token/refresh/",
        AccountTokenRefreshView.as_view(),
        name="api_account_token_refresh"
    ),
    path("password/", include([
        path(
            "change/",
            AccountChangePasswordView.as_view(),
            name="api_account_password_change"
        ),
        path(
            "forgot/",
            include([
                path(
                    '',
                    AccountForgotPasswordView.as_view(),
                    name="api_account_password_forgot"
                ),
                path(
                    "verify/",
                    AccountForgotPasswordVerifyView.as_view(),
                    name="api_account_password_forgot_verify"
                )
            ])
        ),
        path(
            "reset/",
            AccountResetPasswordView.as_view(),
            name="api_account_password_reset"
            )
    ]))
]
