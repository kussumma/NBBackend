import requests
from django.conf import settings


class RecaptchaHelper:
    def __init__(self, recaptcha):
        self.recaptcha = recaptcha
        self.recaptcha_secret = settings.RECAPTCHA_SECRET_KEY

    def validate(self):
        try:
            recaptcha_response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": self.recaptcha_secret,
                    "response": self.recaptcha,
                },
            )
            recaptcha_response = recaptcha_response.json()

            return recaptcha_response

        except Exception as e:
            return e
