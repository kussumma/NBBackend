from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()

class UserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


