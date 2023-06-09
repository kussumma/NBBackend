from rest_framework import serializers

from .models import (
    DiscountType,
    Coupon,
    CouponUser,
    CouponBanner
)

class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountType
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ['code', 'hashed_code']

class CouponUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUser
        fields = '__all__'
        read_only_fields = ['user']

class CouponBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponBanner
        fields = '__all__'