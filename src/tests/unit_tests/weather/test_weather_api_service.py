from unittest.mock import MagicMock

import pytest
from requests.exceptions import RequestException
from rest_framework.exceptions import ValidationError

from weather.services.weather_api import WeatherConnector, get_weather


def test_fetch_weather_by_postal_code_success(
    mock_requests_get: MagicMock,
) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"weather": "sunny"}
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    weather_connector = WeatherConnector()
    result = weather_connector.fetch_weather_by_postal_code("12345", "US")
    assert result == {"weather": "sunny"}


def test_fetch_weather_by_postal_code_failure(
    mock_requests_get: MagicMock,
) -> None:
    mock_requests_get.side_effect = RequestException("Error")

    weather_connector = WeatherConnector()
    with pytest.raises(ValidationError):
        weather_connector.fetch_weather_by_postal_code("invalid", "US")


def test_get_weather_fetch_and_cache(mock_requests_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"weather": "sunny"}
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    result = get_weather("12345", "US")
    assert result == {"weather": "sunny"}

    # Ensure the data is cached
    mock_response.json.return_value = {"weather": "rainy"}
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response
    result = get_weather("12345", "US")
    assert result == {"weather": "sunny"}
