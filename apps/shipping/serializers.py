from rest_framework import serializers
from .models import Shipping, ShippingRoute
from django.contrib.auth import get_user_model

User = get_user_model()

class ShippingRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRoute
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ShippingSerializer(serializers.ModelSerializer):
    origin = ShippingRouteSerializer(read_only=True)
    destination = ShippingRouteSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = '__all__'
        read_only_fields = ['order', 'created_at', 'updated_at']

class ShippingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'
        read_only_fields = ['user']