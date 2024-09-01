from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from parcel.models import Address, Article, UserShipment
from parcel.serializers import (
    AddressSerializer,
    ArticleSerializer,
    UserShipmentSerializer,
)
from utils.base_views import BaseUserOwnedViewSet
from utils.permissions import AllowObjOwnerReadOnly


class AddressViewSet(ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]
    filterset_fields = ["street", "city", "country", "postal_code"]


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    filterset_fields = ["name", "price", "sku"]


class UserShipmentViewSet(BaseUserOwnedViewSet):
    queryset = UserShipment.objects.all()
    serializer_class = UserShipmentSerializer
    permission_classes = [AllowObjOwnerReadOnly]
    filterset_fields = [
        "user",
        "article",
        "carrier",
        "status",
        "tracking_number",
    ]
