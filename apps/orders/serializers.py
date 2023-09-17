from rest_framework import serializers

from .models import Order, OrderItem, ReturnOrder, RefundOrder, ReturnImage, ShippingOrder

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class ShippingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOrder
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_order = ShippingOrderSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['ref_code', 'user']

class ReturnImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnImage
        fields = '__all__'

class ReturnOrderSerializer(serializers.ModelSerializer):
    return_images = ReturnImageSerializer(many=True, read_only=True)
    class Meta:
        model = ReturnOrder
        fields = '__all__'
        read_only_fields = ['user']

class RefundOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundOrder
        fields = '__all__'
