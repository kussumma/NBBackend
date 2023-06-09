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
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = '__all__'
        read_only_fields = ['slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['slug']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        read_only_fields = ['slug']

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user']

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = BasicUserSerializer(user)
        return user_serializer.data

class WishlistSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['user']

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = BasicUserSerializer(user)
        return user_serializer.data

class ProductSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField(read_only=True)
    max_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'