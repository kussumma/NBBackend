from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["cart", "product"]

    def get_product_data(self, obj):
        product = obj.product
        stock = obj.stock
        product_data = {
            "name": product.name,
            "sku": stock.sku,
            "slug": product.slug,
            "image": product.cover.url or None,
            "price": stock.price,
            "discount": stock.discount,
            "size": stock.size or None,
            "color": stock.color or None,
            "variant": stock.variant or None,
        }
        return product_data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["user"]
