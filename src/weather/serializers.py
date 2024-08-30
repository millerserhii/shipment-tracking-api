# pylint: disable=W0223
from rest_framework import serializers


class WeatherRequestSerializer(serializers.Serializer):
    postal_code = serializers.CharField(max_length=10)
    country = serializers.CharField(max_length=3)
