import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from model_bakery import baker
from rest_framework.test import APIClient


UserModel = get_user_model()


@pytest.fixture
def user() -> AbstractBaseUser:
    return baker.make(UserModel)


@pytest.fixture
def superuser() -> AbstractBaseUser:
    return baker.make(UserModel, is_superuser=True)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def auth_api_client(
    user: AbstractBaseUser,  # pylint: disable=redefined-outer-name
) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_api_client_superuser(
    superuser: AbstractBaseUser,  # pylint: disable=redefined-outer-name
) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=superuser)
    return client


@pytest.fixture
def http_request() -> HttpRequest:
    """
    Fixture to provide a mock HttpRequest object.
    """
    request = HttpRequest()
    request.method = "GET"
    request.path = "/test-url/"
    return request
