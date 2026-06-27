
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path(
        "auth/accounts/", include("accounts.urls")
    ),
    path("schema/", SpectacularAPIView.as_view(), name="api_schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="api_schema"),
        name="api_docs"
    ),
]
