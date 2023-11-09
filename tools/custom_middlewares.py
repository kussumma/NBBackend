from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import reverse
import json


class BearerTokenMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_AUTHORIZATION" not in request.META:
            access_token = request.COOKIES.get(settings.REST_AUTH["JWT_AUTH_COOKIE"])
            if access_token:
                request.META["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        response = self.get_response(request)
        return response


class AccessTokenToBodyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path == reverse("token_verify")
            and request.method == "POST"
            and "token" not in request.POST
        ):
            access_token = request.COOKIES.get(settings.REST_AUTH["JWT_AUTH_COOKIE"])
            if access_token:
                body = json.loads(request.body)
                body["token"] = access_token
                request._body = json.dumps(body).encode("utf-8")
        response = self.get_response(request)
        return response


class RefreshTokenToBodyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.path = [reverse("token_refresh"), reverse("rest_logout")]

    def __call__(self, request):
        if (
            request.path in self.path
            and request.method == "POST"
            and "refresh" not in request.POST
        ):
            refresh_token = request.COOKIES.get(
                settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]
            )
            if refresh_token:
                body = json.loads(request.body)
                body["refresh"] = refresh_token
                request._body = json.dumps(body).encode("utf-8")
        response = self.get_response(request)
        return response
