from rest_framework import serializers

from .models import (
    DiscountType,
    Coupon,
    CouponUser,
    Promo,
    PromoBanner
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

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'

class PromoBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoBanner
        fields = '__all__'