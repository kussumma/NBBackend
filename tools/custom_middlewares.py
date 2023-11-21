from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
import json
from tools.recaptcha_helper import RecaptchaHelper


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


class ReCaptchaMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_path = [
            reverse("rest_login"),
            reverse("rest_register"),
            reverse("rest_password_reset"),
            reverse("subscription-list"),
        ]
        self.request_method = ["POST"]

    def __call__(self, request):
        if (
            request.method in self.request_method
            and request.path in self.protected_path
        ):
            # get recaptcha token from body
            recaptcha = json.loads(request.body).get("recaptcha", None)

            if not recaptcha:
                return JsonResponse(
                    {"error": "reCAPTCHA token is required"}, status=400
                )

            recaptcha_helper = RecaptchaHelper(recaptcha)
            recaptcha_response = recaptcha_helper.validate()

            if not recaptcha_response.get("success", False):
                return JsonResponse(
                    {"error": "reCAPTCHA validation failed"}, status=400
                )

            if recaptcha_response.get("score", 0) < 0.8:
                return JsonResponse({"error": "reCAPTCHA score is too low"}, status=400)

        response = self.get_response(request)
        return response
