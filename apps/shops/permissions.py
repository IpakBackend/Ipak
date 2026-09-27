from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from .models import Shop


class IsShopOwner(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:  # type:ignore
        return Shop.objects.filter(
            pk=view.kwargs["pk"],
            owner=request.user
        ).exists()
