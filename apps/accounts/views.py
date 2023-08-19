from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import filters

from .serializers import UserSerializer

User = get_user_model()

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