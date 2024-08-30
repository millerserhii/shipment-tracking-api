import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_ping(api_client: APIClient) -> None:
    url = reverse("ping")
    response = api_client.get(url)
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content["ping"] == "pong!"
