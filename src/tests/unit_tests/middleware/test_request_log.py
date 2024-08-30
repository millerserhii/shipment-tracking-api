import json
import logging
from unittest.mock import MagicMock

import pytest
from django.test import RequestFactory

from backend.middleware.request_log import RequestLogMiddleware


def test_middleware_logging_successful_request(
    caplog: pytest.LogCaptureFixture,
    request_log_middleware: RequestLogMiddleware,
    request_factory: RequestFactory,
    mocker: MagicMock,
) -> None:
    mocker.patch("socket.gethostname", return_value="test-server")

    # Use POST instead of GET to include JSON body
    request = request_factory.post(
        "/api/test/",
        data=json.dumps({"key": "value"}),
        content_type="application/json",
    )
    request.META["REMOTE_ADDR"] = "127.0.0.1"

    with caplog.at_level(logging.INFO):
        response = request_log_middleware(request)
        assert response.status_code == 200

    assert len(caplog.records) == 1
    log_record = caplog.records[0]
    assert log_record.levelname == "INFO"
    assert log_record.message.startswith("{'request_method': 'POST'")
    assert "test-server" in log_record.message


def test_middleware_process_exception_logs_error(
    caplog: pytest.LogCaptureFixture,
    request_log_middleware: RequestLogMiddleware,
    request_factory: RequestFactory,
    mocker: MagicMock,
) -> None:
    mocker.patch("socket.gethostname", return_value="test-server")
    request = request_factory.get("/api/test/")
    request.META["REMOTE_ADDR"] = "127.0.0.1"

    exception = Exception("Test exception")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(Exception, match="Test exception"):
            request_log_middleware.process_exception(request, exception)

    assert len(caplog.records) == 1
    log_record = caplog.records[0]
    assert log_record.levelname == "ERROR"
    assert "Unhandled Exception: Test exception" in log_record.message
