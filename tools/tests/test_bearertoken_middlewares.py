import pytest
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from tools.custom_middlewares import BearerTokenMiddleware


@pytest.fixture
def http_request():
    return HttpRequest()


@pytest.fixture
def http_response():
    return HttpResponse()


@pytest.fixture
def get_response():
    def _get_response(request):
        return HttpResponse()

    return _get_response


def test_bearer_token_middleware_adds_token_to_header(http_request, get_response):
    # Arrange
    middleware = BearerTokenMiddleware(get_response)
    http_request.COOKIES[settings.REST_AUTH["JWT_AUTH_COOKIE"]] = "access_token"

    # Act
    middleware(http_request)

    # Assert
    assert "HTTP_AUTHORIZATION" in http_request.META
    assert http_request.META["HTTP_AUTHORIZATION"] == "Bearer access_token"


def test_bearer_token_middleware_does_not_add_token_when_already_present(
    http_request, get_response
):
    # Arrange
    middleware = BearerTokenMiddleware(get_response)
    http_request.META["HTTP_AUTHORIZATION"] = "Bearer existing_token"
    http_request.COOKIES[settings.REST_AUTH["JWT_AUTH_COOKIE"]] = "access_token"

    # Act
    middleware(http_request)

    # Assert
    assert "HTTP_AUTHORIZATION" in http_request.META
    assert http_request.META["HTTP_AUTHORIZATION"] == "Bearer existing_token"


def test_bearer_token_middleware_does_not_add_token_when_cookie_not_present(
    http_request, get_response
):
    # Arrange
    middleware = BearerTokenMiddleware(get_response)

    # Act
    middleware(http_request)

    # Assert
    assert "HTTP_AUTHORIZATION" not in http_request.META


def test_bearer_token_middleware_calls_get_response_and_returns_response(
    http_request, http_response
):
    # Arrange
    middleware = BearerTokenMiddleware(lambda req: http_response)

    # Act
    actual_response = middleware(http_request)

    # Assert
    assert actual_response == http_response
