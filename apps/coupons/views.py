from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from tools.custom_permissions import IsAdminOrReadOnly

from .models import (
    DiscountType,
    Coupon,
    CouponUser,
    CouponBanner
)

from .serializers import (
    DiscountTypeSerializer,
    CouponSerializer,
    CouponUserSerializer,
    CouponBannerSerializer
)

class DiscountTypeViewSet(viewsets.ModelViewSet):
    queryset = DiscountType.objects.all()
    serializer_class = DiscountTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['code', 'name']
    ordering_fields = ['name', 'code', 'valid_from', 'valid_to']
    filterset_fields = {
        'discount_type': ['exact'],
        'code': ['exact'],
        'is_active': ['exact'],
        'valid_from': ['exact', 'gte', 'lte'],
        'valid_to': ['exact', 'gte', 'lte'],
    }
    ordering = ['name', 'code', 'valid_from', 'valid_to']

class CouponUserViewSet(viewsets.ModelViewSet):
    queryset = CouponUser.objects.all()
    serializer_class = CouponUserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['coupon__code', 'user__email']
    ordering_fields = ['coupon__code', 'user__email']

class CouponBannerViewSet(viewsets.ModelViewSet):
    queryset = CouponBanner.objects.all()
    serializer_class = CouponBannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['coupon__name', 'id']
    ordering_fields = ['coupon__name', 'id']
    ordering = ['coupon__name', 'id']