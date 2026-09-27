from django.urls import include, path

from .views import (
    ProductListView,
    ProductRetrieveUpdateView,
    ShopListCreateView,
    ShopMyView,
    ShopProductListCreateView,
    ShopRetrieveUpdateView,
)

urlpatterns = [
    path('', ShopListCreateView.as_view()),
    path("my/", ShopMyView.as_view()),
    path("products/", include([
        path('', ProductListView.as_view()),
        path("<int:pk>/", ProductRetrieveUpdateView.as_view())
    ])),
    path("<int:pk>/", include([
        path('', ShopRetrieveUpdateView.as_view()),
        path("products/", ShopProductListCreateView.as_view())
    ]))
]
