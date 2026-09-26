from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Color, Shop
from .serializers import ColorSerializer, ShopSerializer

# Create your views here.


class ColorListView(ListAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class ShopCreateView(CreateAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()


class ShopMyView(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ShopSerializer

    def get_queryset(self) -> QuerySet[Shop]:  # type:ignore
        return Shop.objects.filter(owner=self.request.user)
