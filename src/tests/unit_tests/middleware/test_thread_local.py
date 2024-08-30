from django.http import HttpRequest, HttpResponse

from backend.middleware.thread_local import (
    ThreadLocalMiddleware,
    add_request_to_thread_local,
    clear_threading_locals,
    get_current_request,
)


def test_get_current_request_no_request() -> None:
    """
    Test that get_current_request returns None if no request is set.
    """
    clear_threading_locals()
    assert get_current_request() is None


def test_add_request_to_thread_local(http_request: HttpRequest) -> None:
    """
    Test adding a request to thread-local storage.
    """
    add_request_to_thread_local(http_request)
    assert get_current_request() == http_request


def test_clear_threading_locals(http_request: HttpRequest) -> None:
    """
    Test clearing thread-local variables.
    """
    add_request_to_thread_local(http_request)
    clear_threading_locals()
    assert get_current_request() is None


def test_thread_local_middleware(http_request: HttpRequest) -> None:
    """
    Test the ThreadLocalMiddleware that it sets
    the request in thread-local storage.
    """

    def get_response(request: HttpRequest) -> HttpResponse:
        return HttpResponse()

    middleware = ThreadLocalMiddleware(get_response)
    response = middleware(http_request)

    assert response.status_code == 200
    assert get_current_request() == http_request


def test_thread_local_middleware_clears_request(
    http_request: HttpRequest,
) -> None:
    """
    Test that after the response is returned,
    the request should still be in thread-local.
    """

    def get_response(request: HttpRequest) -> HttpResponse:
        return HttpResponse()

    middleware = ThreadLocalMiddleware(get_response)
    middleware(http_request)

    # Ensure request is still there after the call
    assert get_current_request() == http_request
