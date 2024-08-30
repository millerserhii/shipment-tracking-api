from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_weather_view_success(
    api_client: APIClient, mock_requests_get: MagicMock
) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"weather": "sunny"}
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    url = reverse("get-weather")
    response = api_client.get(url, {"postal_code": "90766", "country": "DE"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"weather": "sunny"}


def test_weather_view_missing_query_params(api_client: APIClient) -> None:
    url = reverse("get-weather")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response.data, dict)
    assert "postal_code" in response.data
    assert "country" in response.data
