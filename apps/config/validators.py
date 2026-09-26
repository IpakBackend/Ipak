from django.core.validators import MinLengthValidator, RegexValidator

name_validator = RegexValidator(
    regex=r"^[A-ZА-Я][a-zа-яё'-]+$",
    message="Only letters, ' or - characters, and must start with an uppercase letter.",
    code="invalid_name",
)

latin_username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message="Username must contain only Latin letters and numbers.",
)

name_validators = [name_validator]

username_validators = [
    MinLengthValidator(
        limit_value=3, message="Must be at least 3 characters long."
    ),
    latin_username_validator,
]

hexadecimal_validator = RegexValidator(
    regex=r"^[0-9A-F]{6}$",
    message="Enter a valid hexadecimal color (e.g. FF0000)."
)
