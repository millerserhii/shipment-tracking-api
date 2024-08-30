import logging
from typing import Any, Optional

import requests
from django.conf import settings
from requests.exceptions import HTTPError, RequestException, Timeout
from rest_framework.exceptions import ValidationError

from utils.cache_utils import get_cached_weather, set_cached_weather


logger = logging.getLogger("main")


class WeatherConnector:
    """
    Connector class to get weather data from the weather API
    Uses Singleton pattern to avoid multiple instances
    """

    _instance = None

    def __new__(cls) -> "WeatherConnector":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self.api_key: str = settings.WEATHER_API_KEY
            self.url: str = settings.WEATHER_API_URL
            self._initialized = True

    def fetch_weather_by_postal_code(
        self, postal_code: str, country: str
    ) -> dict[str, Any]:
        logger.debug("Getting weather data for %s, %s", postal_code, country)
        try:
            response = requests.get(
                self.url,
                params={
                    "postal_code": postal_code,
                    "country": country,
                    "key": self.api_key,
                },
                timeout=5,
            )
            response.raise_for_status()
            return response.json()
        except (RequestException, Timeout, HTTPError) as e:
            logger.error("Error in getting weather data: %s", e)
            raise ValidationError("Error in getting weather data") from e


def get_weather(postal_code: str, country: str) -> dict[str, Any]:
    weather_data: Optional[dict[str, Any]] = get_cached_weather(
        postal_code, country
    )

    if not weather_data:
        weather_connector = WeatherConnector()
        weather_data = weather_connector.fetch_weather_by_postal_code(
            postal_code, country
        )
        set_cached_weather(postal_code, country, weather_data)

    return weather_data
