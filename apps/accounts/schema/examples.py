from drf_spectacular.utils import OpenApiExample

signup_validation_error_example = OpenApiExample(name="Validation error", value={
    "type": "validation_error",
    "errors": [
        {
            "code": "required",
            "detail": "This field is required.",
            "attr": "username"
        },
        {
            "code": "required",
            "detail": "This field is required.",
            "attr": "password"
        }
    ]
})

login_authentication_failed_error_example = OpenApiExample(name="Authentication failed", value={
    "type": "client_error",
    "errors": [{
        "code": "authentication_failed",
        "detail": "Invalid credentials",
        "attr": None
    }]
})

logout_validation_error_example = OpenApiExample(name="Validation error", value={
    "type": "validation_error",
    "errors": [{
        "code": "invalid",
        "detail": "Invalid refresh token",
        "attr": "refresh_token"
    }]
})

not_authenticated_error_example = OpenApiExample(name="Not authenticated", value={
    "type": "client_error",
    "errors": [{
        "code": "not_authenticated",
        "detail": "Authentication credentials were not provided.",
        "attr": None
    }]
})

token_not_valid_error_example = OpenApiExample(name="Validation error", value={
    "type": "client_error",
    "errors": [{
        "code": "invalid",
        "detail": "Token is invalid",
        "attr": None
    }]
})

email_not_found_error_example = OpenApiExample(name="Not found", value={
    "type": "validation_error",
    "errors": [{
        "code": "not_found",
        "detail": "Account with such email does not exist",
        "attr": "email"
    }]
})

invalid_email_error_example = OpenApiExample(name="Validation error", value={
    "type": "validation_error",
    "errors": [{
        "code": "invalid",
        "detail": "Failed to send email",
        "attr": "email"
    }]
})

otp_rate_limited_error_example = OpenApiExample(name="Too many requests", value={
    "type": "client_error",
    "errors": [{
        "code": "otp_rate_limited",
        "detail": "You already have an existing OTP code. Please wait before generating a new one.",
        "attr": None
    }]
})

reset_rate_limited_error_example = OpenApiExample(name="Too many requests", value={
    "type": "client_error",
    "errors": [{
        "code": "reset_rate_limited",
        "detail": "You already have an existing reset token. Please wait before generating a new one.",
        "attr": None
    }]
})

invalid_reset_token_error_example = OpenApiExample(name="Validation error", value={
    "type": "client_error",
    "errors": [{
        "code": "invalid",
        "detail": "Invalid reset token.",
        "attr": "token"
    }]
})

non_field_email_not_found_error_example = OpenApiExample(name="Not found", value={
    "type": "validation_error",
    "errors": [{
        "code": "not_found",
        "detail": "Account with such email does not exist",
        "attr": None
    }]
})
