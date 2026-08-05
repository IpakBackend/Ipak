from config.serializers import StandardizedErrorResponseSerializer
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_429_TOO_MANY_REQUESTS,
)

from ..serializers import (
    AccountChangePasswordSerializer,
    AccountForgotPasswordSerializer,
    AccountForgotPasswordVerifySerializer,
    AccountLoginSerializer,
    AccountLogoutSerializer,
    AccountResetPasswordSerializer,
    AccountSerializer,
    AccountTokenRefreshSerializer,
    AccountVerifyEmailSerializer,
)
from .examples import (
    email_not_found_error_example,
    invalid_email_error_example,
    invalid_reset_token_error_example,
    login_authentication_failed_error_example,
    logout_validation_error_example,
    non_field_email_not_found_error_example,
    not_authenticated_error_example,
    otp_rate_limited_error_example,
    reset_rate_limited_error_example,
    signup_validation_error_example,
    token_not_valid_error_example,
)
from .responses import not_authenticated_response

account_signup_schema = extend_schema_view(
    post=extend_schema(
        request=AccountSerializer,
        responses={
            HTTP_201_CREATED: AccountSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Validation error",
                examples=[signup_validation_error_example]
            )
        }
    )
)

account_verify_email_schema = extend_schema_view(
    post=extend_schema(
        request=AccountVerifyEmailSerializer,
        responses={
            HTTP_200_OK: AccountVerifyEmailSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Validation error",
                examples=[]
            )
        }
    )
)

account_login_schema = extend_schema_view(
    post=extend_schema(
        request=AccountLoginSerializer,
        responses={
            HTTP_201_CREATED: AccountLoginSerializer,
            HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Authentication failed",
                examples=[login_authentication_failed_error_example]
            )
        }
    )
)

account_logout_schema = extend_schema_view(
    post=extend_schema(
        request=AccountLogoutSerializer,
        responses={
            HTTP_204_NO_CONTENT: None,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Validation error",
                examples=[logout_validation_error_example]
            )
        }
    )
)

account_me_schema = extend_schema_view(
    get=extend_schema(
        responses={
            HTTP_200_OK: AccountSerializer,
            HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Not authenticated",
                examples=[not_authenticated_error_example]
            )
        }
    )
)

# account_token_refresh_schema = extend_schema_view(
#     post=extend_schema(
#         responses={
#             HTTP_200_OK: AccountTokenRefreshSerializer,
#             HTTP_400_BAD_REQUEST: not_authenticated_response
#         }
#     )
# )

account_change_password_schema = extend_schema_view(
    post=extend_schema(
        request=AccountChangePasswordSerializer,
        responses={
            HTTP_200_OK: AccountChangePasswordSerializer,
            HTTP_401_UNAUTHORIZED: not_authenticated_response
        }
    )
)

account_forgot_password_schema = extend_schema_view(
    post=extend_schema(
        request=AccountForgotPasswordSerializer,
        responses={
            HTTP_200_OK: AccountForgotPasswordSerializer,
            HTTP_404_NOT_FOUND: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Not found",
                examples=[email_not_found_error_example]),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Validation error",
                examples=[invalid_email_error_example]
            ),
            HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Too many requests",
                examples=[otp_rate_limited_error_example]
            )
        }
    )
)

account_forgot_password_verify_schema = extend_schema_view(
    post=extend_schema(
        request=AccountForgotPasswordVerifySerializer,
        responses={
            HTTP_200_OK: AccountForgotPasswordVerifySerializer,
            HTTP_404_NOT_FOUND: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Not found",
                examples=[email_not_found_error_example]),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Validation error",
                examples=[invalid_email_error_example]
            ),
            HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Too many requests",
                examples=[reset_rate_limited_error_example]
            )
        }
    )
)

account_password_reset_schema = extend_schema_view(
    patch=extend_schema(
        request=AccountResetPasswordSerializer,
        responses={
            HTTP_200_OK: AccountResetPasswordSerializer,
            HTTP_404_NOT_FOUND: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Not found",
                examples=[non_field_email_not_found_error_example]
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=StandardizedErrorResponseSerializer,
                description="Validation error",
                examples=[invalid_reset_token_error_example]
            )
        }
    )
)
