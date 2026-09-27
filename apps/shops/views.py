from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from .filters import ProductFilter, ShopFilter
from .models import Color, Product, Shop
from .permissions import IsShopOwner
from .serializers import ColorSerializer, ProductSerializer, ShopSerializer

# Create your views here.


class ColorListView(ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ShopListCreateView(ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filterset_class = ShopFilter

    def get_permissions(self) -> list[BasePermission]:
        if self.request.method == "POST":
            return [IsAuthenticated()]

        return [AllowAny()]


class ShopRetrieveUpdateView(RetrieveUpdateAPIView):
    http_method_names = ["get", "patch"]
    serializer_class = ShopSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.request.method == "PATCH":
            return [IsAuthenticated()]

        return [AllowAny()]

    def get_queryset(self) -> QuerySet[Shop]:  # type:ignore
        if self.request.method == "PATCH":
            return Shop.objects.filter(owner=self.request.user)

        return Shop.objects.all()


class ShopMyView(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ShopSerializer

    def get_queryset(self) -> QuerySet[Shop]:  # type:ignore
        if getattr(self, "swagger_fake_view", False):
            return Shop.objects.all()

        return Shop.objects.filter(owner=self.request.user)


class ShopProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_permissions(self) -> list[BasePermission]:
        if self.request.method == "POST":
            return [IsAuthenticated(), IsShopOwner()]

        return [AllowAny()]

    def get_queryset(self) -> QuerySet[Product]:  # type: ignore
        if getattr(self, "swagger_fake_view", False):
            return Product.objects.all()

        return Product.objects.filter(shop=self.kwargs["pk"])

    def perform_create(self, serializer) -> None:
        shop: Shop = get_object_or_404(klass=Shop, pk=self.kwargs["pk"])
        serializer.save(shop=shop)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


class ProductRetrieveUpdateView(RetrieveUpdateAPIView):
    http_method_names = ["get", "patch"]
    serializer_class = ProductSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.request.method == "PATCH":
            return [IsAuthenticated()]

        return [AllowAny()]

    def get_queryset(self) -> QuerySet[Product]:  # type:ignore
        if self.request.method == "PATCH":
            return Product.objects.filter(shop__owner=self.request.user)

        return Product.objects.all()
