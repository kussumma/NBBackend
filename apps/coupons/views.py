from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from tools.custom_permissions import IsAdminOrReadOnly

from .models import DiscountType, Coupon, CouponUser, Promotion

from .serializers import (
    DiscountTypeSerializer,
    CouponSerializer,
    CouponUserSerializer,
    PromotionSerializer,
)


class DiscountTypeViewSet(viewsets.ModelViewSet):
    queryset = DiscountType.objects.all()
    serializer_class = DiscountTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "prefix_code", "created_at", "updated_at"]
    ordering_fields = ["name", "created_at", "updated_at"]
    filterset_fields = {
        "name": ["exact", "icontains"],
        "prefix_code": ["exact"],
        "discount_type": ["exact"],
        "is_active": ["exact"],
        "valid_from": ["exact", "gte", "lte"],
        "valid_to": ["exact", "gte", "lte"],
    }
    ordering = ["name", "created_at", "updated_at"]

    def get_queryset(self):
        queryset = Coupon.objects.filter(is_active=True, is_private=False)
        return queryset


class CouponUserViewSet(viewsets.ModelViewSet):
    queryset = CouponUser.objects.all()
    serializer_class = CouponUserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["coupon__prefix_code", "user__email"]
    ordering_fields = ["coupon__prefix_code", "user__email"]


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "created_at", "updated_at"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name", "created_at", "updated_at"]
