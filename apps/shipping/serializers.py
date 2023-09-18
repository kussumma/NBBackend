from rest_framework import serializers
from .models import (
    Shipping, 
    ShippingRoute,
    ShippingGroup,
    ShippingType,
    ShippingGroupItem,
    ShippingGroupTariff
)
from django.contrib.auth import get_user_model

User = get_user_model()

class ShippingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingGroup
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ShippingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ShippingGroupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingGroupItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ShippingGroupTariffSerializer(serializers.ModelSerializer):
    shipping_group_name = serializers.CharField(read_only=True, source='shipping_group.name')
    shipping_type_code = serializers.CharField(read_only=True, source='shipping_type.code')

    class Meta:
        model = ShippingGroupTariff
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

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