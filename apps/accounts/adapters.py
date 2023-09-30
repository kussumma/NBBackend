from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Changing the confirmation URL to fit the domain that we are working on
        """

        url = settings.FRONTEND_URL + "/verify-email/?key=" + emailconfirmation.key

        return url
