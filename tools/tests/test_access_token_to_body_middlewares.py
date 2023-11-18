import json
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from tools.custom_middlewares import AccessTokenToBodyMiddleware


def test_access_token_to_body_middleware_adds_token_to_body_when_conditions_met():
    # Arrange
    middleware = AccessTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = reverse("token_verify")
    request.method = "POST"
    request.COOKIES[settings.REST_AUTH["JWT_AUTH_COOKIE"]] = "access_token"
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    middleware(request)

    # Assert
    modified_body = json.loads(request.body.decode("utf-8"))
    assert "token" in modified_body
    assert modified_body["token"] == "access_token"


def test_access_token_to_body_middleware_does_not_add_token_to_body_when_path_not_token_verify():
    # Arrange
    middleware = AccessTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = "/api/v1/feature-request/"
    request.method = "POST"
    request.POST = {}
    request.COOKIES[settings.REST_AUTH["JWT_AUTH_COOKIE"]] = "access_token"
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    middleware(request)

    # Assert
    modified_body = json.loads(request.body.decode("utf-8"))
    assert "token" not in modified_body


def test_access_token_to_body_middleware_does_not_add_token_to_body_when_method_not_post():
    # Arrange
    middleware = AccessTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = reverse("token_verify")
    request.method = "GET"
    request.POST = {}
    request.COOKIES[settings.REST_AUTH["JWT_AUTH_COOKIE"]] = "access_token"
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    middleware(request)

    # Assert
    modified_body = json.loads(request.body.decode("utf-8"))
    assert "token" not in modified_body


def test_access_token_to_body_middleware_does_not_add_token_to_body_when_token_not_present():
    # Arrange
    middleware = AccessTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()
    request.path = reverse("token_verify")
    request.method = "POST"
    request.POST = {}
    request.COOKIES = {}
    request.META["CONTENT_TYPE"] = "application/json"  # Set content type
    original_body = {}
    request._body = json.dumps(original_body).encode("utf-8")

    # Act
    middleware(request)

    # Assert
    modified_body = json.loads(request.body.decode("utf-8"))
    assert "token" not in request.POST


def test_access_token_to_body_middleware_calls_get_response_and_returns_response():
    # Arrange
    middleware = AccessTokenToBodyMiddleware(lambda req: HttpResponse())
    request = HttpRequest()

    # Act
    response = middleware(request)

    # Assert
    assert isinstance(response, HttpResponse)
