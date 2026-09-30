from django.db.models import QuerySet
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .filters import ProductFilter, ShopFilter
from .models import Color, Product, ProductImage, Shop
from .permissions import IsProductImageOwner, IsProductOwner, IsShopOwner
from .serializers import (
    ColorSerializer,
    ProductImageOrderSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ShopSerializer,
)

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


class ShopDetailView(RetrieveUpdateAPIView):
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


class ProductRetrieveDetailView(RetrieveUpdateAPIView):
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


class ProductProductImageListCreateOrderView(ListCreateAPIView):
    http_method_names = ["get", "post", "put"]
    serializer_class = ProductImageSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.request.method in ["POST", "PUT"]:
            return [IsAuthenticated(), IsProductOwner()]

        return [AllowAny()]

    def get_queryset(self) -> QuerySet[ProductImage]:  # type:ignore
        return ProductImage.objects.filter(product=self.kwargs["pk"])

    @extend_schema(request=ProductImageOrderSerializer, responses=ProductImageSerializer(many=True))
    def put(self, request: Request, *args, **kwargs) -> Response:
        product: Product = get_object_or_404(
            klass=Product,
            pk=self.kwargs["pk"],
        )

        serializer = ProductImageOrderSerializer(
            data=request.data,
            context={"product": product}
        )
        serializer.is_valid(raise_exception=True)

        image_ids: list[int] = \
            serializer.validated_data["images"]  # type:ignore

        queryset = self.get_queryset()

        images: list[ProductImage] = list(queryset)

        images_by_id: dict[int, ProductImage] = {
            image.pk: image for image in images
        }

        size: int = len(images)
        with atomic():
            for image in images:
                image.position += size

            ProductImage.objects.bulk_update(
                objs=images,
                fields=["position"]
            )

            for position, image_id in enumerate(image_ids):
                images_by_id[image_id].position = position

            ProductImage.objects.bulk_update(
                objs=images,
                fields=["position"],
            )

        return Response(data=ProductImageSerializer(
            instance=queryset,
            many=True,
        ).data,
            status=HTTP_200_OK
        )

    def perform_create(self, serializer):
        product: Product = get_object_or_404(
            klass=Product,
            pk=self.kwargs["pk"],
        )

        if product.images.count() >= 3:
            raise ValidationError(
                "A product can have a maximum of 3 images."
            )

        position: int = product.images.count()

        serializer.save(product=product, position=position)


class ProductImageDetailView(RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated(), IsProductImageOwner()]

        return [AllowAny()]
