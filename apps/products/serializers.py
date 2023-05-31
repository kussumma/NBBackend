from rest_framework import serializers

from .models import (
    Category,
    Subcategory,
    Tag,
    Brand,
    Product,
    Rating,
    Wishlist,
    Stock
)
from apps.accounts.serializers import BasicUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField(read_only=True)
    max_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'