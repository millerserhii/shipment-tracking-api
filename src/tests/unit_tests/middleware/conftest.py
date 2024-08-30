from collections.abc import Callable
from unittest.mock import MagicMock

import pytest
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory

from backend.middleware.request_log import RequestLogMiddleware


# pylint: disable=redefined-outer-name
@pytest.fixture
def mock_get_response() -> Callable[[HttpRequest], HttpResponse]:
    return MagicMock(return_value=HttpResponse(status=200))


@pytest.fixture
def request_log_middleware(
    mock_get_response: Callable[[HttpRequest], HttpResponse]
) -> RequestLogMiddleware:
    return RequestLogMiddleware(mock_get_response)


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
