from rest_framework import serializers

from .models import DiscountType, Coupon, CouponUser, CouponBanner


class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountType
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    decrypted_code = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def get_decrypted_code(self, obj):
        if not obj.is_private and obj.code:
            try:
                code = obj.code
                decrypted_code = obj.decode_coupon_code(code)
            except:
                decrypted_code = None
        return decrypted_code


class CouponUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUser
        fields = "__all__"
        read_only_fields = ["user"]


class CouponBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponBanner
        fields = "__all__"
