from django.urls import include, path

from .views import (
    ProductImageDetailView,
    ProductListView,
    ProductProductImageListCreateOrderView,
    ProductRetrieveDetailView,
    ShopDetailView,
    ShopListCreateView,
    ShopMyView,
    ShopProductListCreateView,
)

urlpatterns = [
    path('', ShopListCreateView.as_view()),
    path("my/", ShopMyView.as_view()),
    path("products/", include([
        path('', ProductListView.as_view()),
        path("<int:pk>/", include([
            path('', ProductRetrieveDetailView.as_view()),
            path("images/", ProductProductImageListCreateOrderView.as_view())
        ])),
        path("images/<int:pk>/", ProductImageDetailView.as_view())
    ])),
    path("<int:pk>/", include([
        path('', ShopDetailView.as_view()),
        path("products/", ShopProductListCreateView.as_view())
    ]))
]
