import json
import logging
import socket
import time
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


request_logger = logging.getLogger("main")
error_logger = logging.getLogger("error")


class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.monotonic()
        log_data = {
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
        }

        # Only logging "*/api/*" patterns
        if "/api/" in str(request.get_full_path()):
            try:
                if request.body:
                    json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                pass
            except UnicodeDecodeError as e:
                error_logger.warning("UnicodeDecodeError: %s", str(e))

        # request passes on to controller
        response = self.get_response(request)

        # add runtime
        log_data["run_time"] = time.monotonic() - start_time

        request_logger.info(msg=log_data)

        return response

    # Log unhandled exceptions as well
    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> None:
        try:
            raise exception
        except Exception as e:  # pylint: disable=broad-except
            error_logger.exception("Unhandled Exception: %s", str(e))
        raise exception
