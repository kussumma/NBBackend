from rest_framework import serializers

from .models import (
    Category,
    Subcategory,
    Subsubcategory,
    Brand,
    Product,
    Rating,
    Wishlist,
    Stock
)
from apps.accounts.serializers import BasicUserSerializer

class SubsubcategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Subsubcategory
        fields = '__all__'
        read_only_fields = ['slug']

class SubcategorySerializer(serializers.ModelSerializer):
    subsubcategory = SubsubcategorySerializer(many=True, source='subsubcategories', read_only=True)

    class Meta:
        model = Subcategory
        fields = '__all__'
        read_only_fields = ['slug']

class SearchSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(many=True, source='subcategories', read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class SearchCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

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