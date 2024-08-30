from rest_flex_fields import FlexFieldsModelSerializer

from parcel.models import Address, Article, UserShipment


class AddressSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "timestamp",
            "street",
            "city",
            "country",
            "postal_code",
        ]


class ArticleSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "timestamp",
            "name",
            "price",
            "sku",
        ]


class UserShipmentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = UserShipment
        fields = [
            "id",
            "timestamp",
            "user",
            "article",
            "article_quantity",
            "tracking_number",
            "carrier",
            "status",
            "sender_address",
            "receiver_address",
        ]

        expandable_fields = {
            "article": ArticleSerializer,
            "sender_address": AddressSerializer,
            "receiver_address": AddressSerializer,
        }
