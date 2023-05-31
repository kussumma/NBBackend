from rest_framework import serializers

from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer, StockSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.ImageField(source='stock.image', read_only=True)
    product_price = serializers.IntegerField(source='stock.price', read_only=True)
    product_stock = serializers.IntegerField(source='stock.quantity', read_only=True)
    product_size = serializers.CharField(source='stock.size', read_only=True)
    product_color = serializers.CharField(source='stock.color', read_only=True)
    product_other = serializers.CharField(source='stock.other', read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'