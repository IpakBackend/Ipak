from django.urls import include, path

from .views import ShopCreateView, ShopMyView

urlpatterns = [
    path("create/", ShopCreateView.as_view()),
    path("my/", ShopMyView.as_view())
]
