from rest_framework import serializers
from tools.fileupload_helper import validate_uploaded_file

from .models import (
    Category,
    Subcategory,
    Subsubcategory,
    Brand,
    Product,
    Rating,
    Wishlist,
    Stock,
    ExtraProductImage,
)
from apps.accounts.serializers import BasicUserSerializer


class SubsubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsubcategory
        fields = "__all__"
        read_only_fields = ["slug"]

    def validate_cover(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class SubcategorySerializer(serializers.ModelSerializer):
    subsubcategory = SubsubcategorySerializer(
        many=True, source="subsubcategories", read_only=True
    )

    class Meta:
        model = Subcategory
        fields = "__all__"
        read_only_fields = ["slug"]

    def validate_cover(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class SearchSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(
        many=True, source="subcategories", read_only=True
    )

    class Meta:
        model = Category
        fields = "__all__"

    def validate_cover(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class SearchCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        read_only_fields = ["slug"]

    def validate_cover(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Stock
        fields = "__all__"

    def validate_image(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class RatingSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = "__all__"
        read_only_fields = ["user"]

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = BasicUserSerializer(user)
        return user_serializer.data

    def validate_image(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value

    def validate_video(self, value):
        if value:
            validate_uploaded_file(value, "video")
            return value


class WishlistSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = "__all__"
        read_only_fields = ["user"]

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = BasicUserSerializer(user)
        return user_serializer.data

    def get_product_details(self, obj):
        product = obj.product
        product_serializer = ProductSerializer(product)
        return product_serializer.data


class ProductSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField(read_only=True)
    max_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def validate_cover(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


class ExtraProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraProductImage
        fields = "__all__"

    def validate_image(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value
