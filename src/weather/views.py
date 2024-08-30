from typing import Any

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.serializers import WeatherRequestSerializer
from weather.services.weather_api import get_weather


class WeatherView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        serializer = WeatherRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        postal_code: str = serializer.validated_data["postal_code"]
        country: str = serializer.validated_data["country"]

        weather_data: dict[str, Any] = get_weather(postal_code, country)

        return Response(weather_data, status=status.HTTP_200_OK)
