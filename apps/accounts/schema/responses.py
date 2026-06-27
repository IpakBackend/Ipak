from config.serializers import StandardizedErrorResponseSerializer
from drf_spectacular.utils import OpenApiResponse

from .examples import not_authenticated_error_example

not_authenticated_response = OpenApiResponse(
    response=StandardizedErrorResponseSerializer,
    description="Not authenticated error",
    examples=[not_authenticated_error_example]
)

