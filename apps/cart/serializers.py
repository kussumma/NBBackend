from rest_framework import serializers

from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer, StockSerializer

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'