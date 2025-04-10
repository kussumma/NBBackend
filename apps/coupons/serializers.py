from rest_framework import serializers
from tools.fileupload_helper import FileUploadHelper
from .models import DiscountType, Coupon, CouponUser, Promotion


class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountType
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    private_code = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        read_only_fields = ["created_at", "updated_at"]
        exclude = ["code"]

    def get_private_code(self, obj):
        if not obj.is_private:
            code = obj.code
            private_code = obj.decode_coupon_code(code)
        else:
            private_code = None

        return private_code

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class CouponUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUser
        fields = "__all__"
        read_only_fields = ["user"]


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value
