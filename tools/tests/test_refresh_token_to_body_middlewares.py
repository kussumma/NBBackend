import json
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from tools.custom_middlewares import RefreshTokenToBodyMiddleware


def test_refresh_token_to_body_middleware_adds_refresh_token_to_body():
    # Arrange
    middleware = RefreshTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = reverse("token_refresh")
    request.method = "POST"
    request.COOKIES[settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]] = "refresh_token"
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    middleware(request)

    # Assert
    modified_body = json.loads(request.body.decode("utf-8"))
    assert "refresh" in modified_body
    assert modified_body["refresh"] == "refresh_token"


def test_refresh_token_to_body_middleware_does_not_add_refresh_token_to_body_when_not_post_request():
    # Arrange
    middleware = RefreshTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = reverse("token_refresh")
    request.method = "GET"  # Changed to a non-POST method
    request.COOKIES[settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]] = "refresh_token"
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    middleware(request)

    # Assert
    modified_body = json.loads(request._body.decode("utf-8"))
    assert "refresh" not in modified_body


def test_refresh_token_to_body_middleware_does_not_add_refresh_token_to_body_when_refresh_cookie_not_present():
    # Arrange
    middleware = RefreshTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = reverse("token_refresh")
    request.method = "POST"
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    response = middleware(request)

    # Assert
    modified_body = json.loads(request._body.decode("utf-8"))
    assert "refresh" not in modified_body


def test_refresh_token_to_body_middleware_calls_get_response_and_returns_response():
    # Arrange
    middleware = RefreshTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()

    # Act
    response = middleware(request)

    # Assert
    assert isinstance(response, HttpResponse)
