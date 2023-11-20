import json
from django.urls import reverse
from django.http import JsonResponse
from django.test import RequestFactory
import pytest
from tools.custom_middlewares import ReCaptchaMiddleware
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def middleware():
    return ReCaptchaMiddleware(get_response=lambda r: JsonResponse({}))


def test_call_method_request_method_not_in_protected_path(middleware):
    factory = RequestFactory()
    request = factory.post("/v1/feature-request/")
    response = middleware(request)
    assert response.status_code == 200


def test_call_method_request_path_not_in_protected_path(middleware):
    factory = RequestFactory()
    request = factory.get("/v1/top-brands/")
    response = middleware(request)
    assert response.status_code == 200


def test_call_method_recaptcha_token_missing(middleware):
    factory = RequestFactory()
    data = {"username": "test", "password": "test"}
    request = factory.post(
        reverse("rest_login"),
        data=json.dumps(data),
        content_type="application/json",
    )
    response = middleware(request)
    assert response.status_code == 400


def test_call_method_recaptcha_validation_failed(middleware, monkeypatch):
    def mock_validate(self):
        return {"success": False, "error-codes": ["invalid-input-response"]}

    monkeypatch.setattr(
        "tools.custom_middlewares.RecaptchaHelper.validate", mock_validate
    )

    factory = RequestFactory()
    data = {"username": "test", "password": "test", "recaptcha": "token"}
    request = factory.post(
        reverse("rest_login"), data=json.dumps(data), content_type="application/json"
    )
    response = middleware(request)
    assert response.status_code == 400


def test_call_method_recaptcha_score_less_than_0_8(middleware, monkeypatch):
    def mock_validate(self):
        return {"success": True, "score": 0.7}

    monkeypatch.setattr(
        "tools.custom_middlewares.RecaptchaHelper.validate", mock_validate
    )

    factory = RequestFactory()
    data = {"email": "test@mail.com", "password": "test", "recaptcha": "token"}
    request = factory.post(
        reverse("rest_login"), data=json.dumps(data), content_type="application/json"
    )
    response = middleware(request)
    assert response.status_code == 400


def test_call_method_recaptcha_validation_passed(middleware, monkeypatch):
    def mock_validate(self):
        return {"success": True, "score": 0.9}

    monkeypatch.setattr(
        "tools.custom_middlewares.RecaptchaHelper.validate", mock_validate
    )

    factory = RequestFactory()
    data = {"email": "test@mail.com", "password": "test", "recaptcha": "token"}
    request = factory.post(
        reverse("rest_login"), data=json.dumps(data), content_type="application/json"
    )
    response = middleware(request)
    assert response.status_code == 200
