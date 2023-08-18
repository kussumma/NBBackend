from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import filters, status
from rest_framework.response import Response
import requests
from django.shortcuts import redirect
from django.conf import settings

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, VerifyEmailView

from .serializers import UserSerializer

User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.FRONTEND_URL+'/google/'
    client_class = OAuth2Client

class CustomVerifyEmailView(VerifyEmailView):
    def get(self, request, key):
        verify_email_url = settings.BACKEND_URL+'/auth/registration/verify-email/'

        # make a POST request to the verify-email endpoint with the key
        response = requests.post(verify_email_url, {'key': key})
        
        # Redirect user to frontend if the response is successful or not
        if response.status_code == 200:
            redirect_url = settings.FRONTEND_URL+'/signin/'
            return redirect(redirect_url)
        else:
            redirect_url = settings.FRONTEND_URL+'/verification-error/'
            return redirect(redirect_url)

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