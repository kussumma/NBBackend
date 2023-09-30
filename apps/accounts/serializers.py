from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

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


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        read_only_fields = ["user"]
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "user_details"]

    def update(self, instance, validated_data):
        user_details_data = validated_data.pop("user_details", {})
        user_details = instance.user_details

        if user_details_data:
            user_details.avatar = user_details_data.get("avatar", user_details.avatar)
            user_details.phone_number = user_details_data.get(
                "phone_number", user_details.phone_number
            )
            user_details.gender = user_details_data.get("gender", user_details.gender)
            user_details.date_of_birth = user_details_data.get(
                "date_of_birth", user_details.date_of_birth
            )
            user_details.level = user_details_data.get("level", user_details.level)
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


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "avatar", "level"]
