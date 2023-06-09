from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.permissions import (
    IsAdminOrReadOnly,
)

from .models import (
    DiscountType,
    Coupon,
    CouponUser,
    Promo,
    PromoBanner
)

from .serializers import (
    DiscountTypeSerializer,
    CouponSerializer,
    CouponUserSerializer,
    PromoSerializer,
    PromoBannerSerializer
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

class PromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class PromoBannerViewSet(viewsets.ModelViewSet):
    queryset = PromoBanner.objects.all()
    serializer_class = PromoBannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['promo__name', 'id']
    ordering_fields = ['promo__name', 'id']
    ordering = ['promo__name', 'id']