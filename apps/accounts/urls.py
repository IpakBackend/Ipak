from django.urls import include, path

from .views import (
    AccountChangePasswordView,
    AccountForgotPasswordVerifyView,
    AccountForgotPasswordView,
    AccountLoginView,
    AccountLogoutView,
    AccountMeView,
    AccountResetPasswordView,
    AccountSignupView,
    AccountTokenRefreshView,
    AccountVerifyEmailView,
)

urlpatterns = [
    path(
        "signup/",
        AccountSignupView.as_view(),
        name="api-account-signup"
    ),
    path(
        "verify-email/",
        AccountVerifyEmailView.as_view(),
        name="api-account-verify-email"
    ),
    path("login/", AccountLoginView.as_view(), name="api-account-login"),
    path(
        "logout/",
        AccountLogoutView.as_view(),
        name="api-account-logout"
    ),
    path("me/", AccountMeView.as_view(), name="api-account-me"),
    path(
        "token/refresh/",
        AccountTokenRefreshView.as_view(),
        name="api-account-token-refresh"
    ),
    path("password/", include([
        path(
            "change/",
            AccountChangePasswordView.as_view(),
            name="api-account-password-change"
        ),
        path(
            "forgot/",
            include([
                path(
                    '',
                    AccountForgotPasswordView.as_view(),
                    name="api-account-password-forgot"
                ),
                path(
                    "verify/",
                    AccountForgotPasswordVerifyView.as_view(),
                    name="api-account-password-forgot-verify"
                )
            ])
        ),
        path(
            "reset/",
            AccountResetPasswordView.as_view(),
            name="api-account-password-reset"
        )
    ]))
]
