from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework import filters
from django.conf import settings

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .serializers import UserSerializer

User = get_user_model()


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.FRONTEND_URL + "/google/"
    client_class = OAuth2Client


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email", "first_name", "last_name"]
    ordering = ["-date_joined"]

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class StaffListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email", "first_name", "last_name"]
    ordering = ["-date_joined"]

    def get_queryset(self):
        return User.objects.filter(is_staff=True)
