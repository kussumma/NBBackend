from rest_framework import serializers
from tools.fileupload_helper import FileUploadHelper

from .models import (
    Order,
    OrderItem,
    ReturnOrder,
    RefundOrder,
    ReturnImage,
    OrderShipping,
)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderShipping
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    order_shipping = OrderShippingSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["ref_code", "user"]


class ReturnImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnImage
        fields = "__all__"

    def validate_image(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class ReturnOrderSerializer(serializers.ModelSerializer):
    return_images = ReturnImageSerializer(many=True, read_only=True)

    class Meta:
        model = ReturnOrder
        fields = "__all__"
        read_only_fields = ["user"]


class RefundOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundOrder
        fields = "__all__"

    def validate_refund_receipt(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value
