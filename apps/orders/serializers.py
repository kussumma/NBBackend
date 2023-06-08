from rest_framework import serializers

from .models import Order, OrderItem, ReturnOrder, RefundOrder, ReturnImage

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class ReturnImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnImage
        fields = '__all__'

class ReturnOrderSerializer(serializers.ModelSerializer):
    return_images = ReturnImageSerializer(many=True, read_only=True)
    class Meta:
        model = ReturnOrder
        fields = '__all__'

class RefundOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundOrder
        fields = '__all__'
