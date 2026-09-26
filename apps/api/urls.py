from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from shops.views import ColorListView

urlpatterns = [
    path(
        "auth/accounts/", include("accounts.urls")
    ),
    path("shops/", include("shops.urls")),

    path("colors/", ColorListView.as_view()),

    path("schema/", SpectacularAPIView.as_view(), name="api_schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="api_schema"),
        name="api_docs"
    )
]
