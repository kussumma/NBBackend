from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from allauth.account.forms import ResetPasswordForm as AllAuthPasswordResetForm
from allauth.account.utils import user_pk_to_url_str
from allauth.account.adapter import get_adapter
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from tools.fileupload_helper import validate_uploaded_file

from .models import UserDetail

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get("first_name")
        user.last_name = self.data.get("last_name")
        user.save()
        return user


class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def _send_unknown_account_mail(self, request, email):
        signup_url = settings.FRONTEND_URL + "/signup/"
        context = {
            "current_site": settings.FRONTEND_URL,
            "email": email,
            "request": request,
            "signup_url": signup_url,
        }
        get_adapter().send_mail("account/email/unknown_account", email, context)

    def _send_password_reset_mail(self, request, email, users, **kwargs):
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in users:
            temp_key = token_generator.make_token(user)

            # send the password reset email
            uid = user_pk_to_url_str(user)
            url = (
                settings.FRONTEND_URL + "/reset-password/" + uid + "/" + temp_key + "/"
            )
            context = {
                "current_site": settings.FRONTEND_URL,
                "user": user,
                "password_reset_url": url,
                "uid": uid,
                "key": temp_key,
                "request": request,
            }
            get_adapter().send_mail("account/email/password_reset_key", email, context)


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomAllAuthPasswordResetForm


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        read_only_fields = ["user"]
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer()

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions", "is_superuser", "is_staff"]

    def update(self, instance, validated_data):
        user_details_data = validated_data.pop("user_details", {})
        user_details = instance.user_details

        if user_details_data:
            user_details.phone_number = user_details_data.get(
                "phone_number", user_details.phone_number
            )
            user_details.gender = user_details_data.get("gender", user_details.gender)
            user_details.date_of_birth = user_details_data.get(
                "date_of_birth", user_details.date_of_birth
            )
            user_details.newsletter = user_details_data.get(
                "newsletter", user_details.newsletter
            )
            user_details.city = user_details_data.get("city", user_details.city)
            user_details.country = user_details_data.get(
                "country", user_details.country
            )
            user_details.language = user_details_data.get(
                "language", user_details.language
            )
            user_details.theme = user_details_data.get("theme", user_details.theme)
            user_details.currency = user_details_data.get(
                "currency", user_details.currency
            )
            user_details.save()

        instance = super().update(instance, validated_data)

        return instance

    def validate_avatar(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "avatar", "level"]
