import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


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

            return Response(recaptcha_response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
