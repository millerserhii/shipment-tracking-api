from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from parcel.models import Address, Article, UserShipment
from weather.services.weather_api import get_weather


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
    receiver_weather = serializers.SerializerMethodField()

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
            "receiver_weather",
        ]

        expandable_fields = {
            "article": ArticleSerializer,
            "sender_address": AddressSerializer,
            "receiver_address": AddressSerializer,
        }

    def get_receiver_weather(self, obj: UserShipment) -> dict[str, str]:
        try:
            return get_weather(
                obj.receiver_address.postal_code, obj.receiver_address.country
            ).get("data")
        except ValidationError:
            return {"error": "Error in getting weather data"}
