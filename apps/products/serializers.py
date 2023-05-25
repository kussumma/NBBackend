from rest_framework import serializers

from apps.accounts.serializers import BasicUserSerializer

from .models import (
    Category,
    Subcategory,
    Brand,
    Product,
    Rating,
    Stock
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
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
    user = BasicUserSerializer()

    class Meta:
        model = Rating
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = '__all__'