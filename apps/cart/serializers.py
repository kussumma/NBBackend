from rest_framework import serializers

from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer, StockSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'

    def get_product_data(self, obj):
        product = obj.product
        stock = obj.stock
        product_data = {
            'name': product.name,
            'slug': product.slug,
            'image': stock.image.url,
            'price': stock.price,
            'discount': product.discount,
            'size': stock.size,
            'color': stock.color,
            'other': stock.other,
        }
        return product_data

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'