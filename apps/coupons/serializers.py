from rest_framework import serializers

from .models import (
    DiscountType,
    Coupon,
    CouponUser
)

class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountType
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUser
        fields = '__all__'