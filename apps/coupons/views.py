from rest_framework import viewsets
from rest_framework import permissions

from .models import (
    DiscountType,
    Coupon,
    CouponUser
)

from .serializers import (
    DiscountTypeSerializer,
    CouponSerializer,
    CouponUserSerializer
)

class DiscountTypeViewSet(viewsets.ModelViewSet):
    queryset = DiscountType.objects.all()
    serializer_class = DiscountTypeSerializer
    permission_classes = [permissions.AllowAny]

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]

class CouponUserViewSet(viewsets.ModelViewSet):
    queryset = CouponUser.objects.all()
    serializer_class = CouponUserSerializer
    permission_classes = [permissions.AllowAny]

