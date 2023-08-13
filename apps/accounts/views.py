from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import filters, status
from rest_framework.response import Response
import requests

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, VerifyEmailView

from .serializers import UserSerializer

User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/google/'
    client_class = OAuth2Client

class VerifyEmailView(VerifyEmailView):
    def get(self, request, key):
        verify_email_url = 'http://127.0.0.1:8000/auth/registration/verify-email/'

        # make a POST request to the verify-email endpoint with the key
        response = requests.post(verify_email_url, {'key': key})
        if response.status_code == 200:
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    def get_queryset(self):
        return User.objects.filter(is_staff=False)
    
class StaffListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    def get_queryset(self):
        return User.objects.filter(is_staff=True)