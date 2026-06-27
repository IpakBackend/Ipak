from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response | None:
    response: Response | None = exception_handler(exc, context)

    if response is None:
        return response

    errors: list[dict[str, str | None]] = []

    if isinstance(exc, ValidationError):
        data = response.data
        print(data)
        if isinstance(data, dict):
            for field, messages in response.data.items():
                if not isinstance(messages, list):
                    messages = [messages]

                for message in messages:
                    errors.append({
                        "code": getattr(message, "code", "invalid"),
                        "detail": str(message),
                        "attr": field,
                    })

        elif isinstance(data, list):
            for message in data:
                errors.append({
                    "code": getattr(message, "code", "invalid"),
                    "detail": str(message),
                    "attr": None,
                })

    elif isinstance(exc, APIException):
        code = exc.get_codes()

        if isinstance(code, dict):
            code = code.get("detail")

        errors.append({
            "code": code,
            "detail": response.data.get("detail"),
            "attr": None,
        })

    response.data = {
        "type": "client_error",
        "errors": errors
    }

    return response
