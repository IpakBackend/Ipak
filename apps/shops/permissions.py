from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from .models import Product, ProductImage, Shop


class IsShopOwner(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:  # type:ignore
        return Shop.objects.filter(
            pk=view.kwargs["pk"],
            owner=request.user
        ).exists()


class IsProductOwner(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:  # type:ignore
        return Product.objects.filter(pk=view.kwargs["pk"], shop__owner=request.user).exists()


class IsProductImageOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: ProductImage):
        return request.user == obj.product.shop.owner
