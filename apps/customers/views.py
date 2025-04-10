from rest_framework import viewsets, serializers
from rest_framework import permissions, filters
from django.contrib.auth import get_user_model

from .models import (
    Favorite,
    Complaint,
    ProductRequest,
    FeatureRequest,
    BugReport,
    Subscription,
)
from .serializers import (
    FavoriteSerializer,
    ComplaintSerializer,
    ProductRequestSerializer,
    FeatureRequestSerializer,
    BugReportSerializer,
    SubscriptionSerializer,
)

User = get_user_model()


class FavoriteViewset(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email", "product__name"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ComplaintViewset(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email", "order__ref_code", "status"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Complaint.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ProductRequestViewset(viewsets.ModelViewSet):
    serializer_class = ProductRequestSerializer
    queryset = ProductRequest.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "status"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return ProductRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class FeatureRequestViewset(viewsets.ModelViewSet):
    serializer_class = FeatureRequestSerializer
    queryset = FeatureRequest.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "status"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return FeatureRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class BugReportViewset(viewsets.ModelViewSet):
    serializer_class = BugReportSerializer
    queryset = BugReport.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "status"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return BugReport.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class SubscriptionViewset(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["email"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.AllowAny]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # check if email already exists
        email = self.request.data.get("email")
        if Subscription.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "This email is already subscribed"}
            )
        serializer.save()
