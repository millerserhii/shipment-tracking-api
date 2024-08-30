import threading
from collections.abc import Callable
from typing import Optional

from django.http import HttpRequest, HttpResponse


_thread_local = threading.local()


def get_current_request() -> Optional[HttpRequest]:
    """
    Retrieves the current HttpRequest object from thread-local storage.

    This function is typically used to access the request object outside of
    the view layer, such as in models or utility functions, where the request
    object is not directly available.

    Returns:
        HttpRequest: The current request object, if available. Otherwise, None.
    """
    return getattr(_thread_local, "request", None)


def clear_threading_locals() -> None:
    """
    Clears all thread-local variables.

    This function is typically used in tests to clear the thread-local storage
    between test runs.
    """
    _thread_local.__dict__.clear()


def add_request_to_thread_local(request: HttpRequest) -> None:
    """
    Adds the request object to thread-local storage.

    This function is typically used in tests to add the request object to
    thread-local storage.
    """
    _thread_local.request = request


class ThreadLocalMiddleware:
    """
    Middleware to store the request object in thread-local storage.

    This middleware captures the current HttpRequest object and stores it
    in a thread-local variable, making it accessible throughout the lifecycle
    of the request. It is useful for accessing the request object in places
    where it is not directly passed, like signal handlers or model methods.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        _thread_local.request = request
        response = self.get_response(request)
        return response
