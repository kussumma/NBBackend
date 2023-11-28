from rest_framework import serializers
from tools.fileupload_helper import FileUploadHelper

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
    ExtraProductVideo,
)
from apps.accounts.serializers import BasicUserSerializer


class SubsubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsubcategory
        fields = "__all__"
        read_only_fields = ["slug"]

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class SubcategorySerializer(serializers.ModelSerializer):
    subsubcategory = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = "__all__"
        read_only_fields = ["slug"]

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value

    def get_subsubcategory(self, obj):
        subsubcategory = Subsubcategory.objects.filter(subcategory=obj).order_by("name")
        subsubcategory_serializer = SubsubcategorySerializer(subsubcategory, many=True)
        return subsubcategory_serializer.data


class SearchSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value

    def get_subcategory(self, obj):
        subcategory = Subcategory.objects.filter(category=obj).order_by("name")
        subcategory_serializer = SubcategorySerializer(subcategory, many=True)
        return subcategory_serializer.data


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
            value = FileUploadHelper(value, webp=True).validate()
            return value

    def validate_logo(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Stock
        fields = "__all__"


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
            value = FileUploadHelper(value, webp=True).validate()
            return value

    def validate_video(self, value):
        if value:
            value = FileUploadHelper(value, "video").validate()
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
            value = FileUploadHelper(value, webp=True).validate()
            return value


class ExtraProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraProductImage
        fields = "__all__"

    def validate_image(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class ExtraProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraProductVideo
        fields = "__all__"

    def validate_video(self, value):
        if value:
            value = FileUploadHelper(value, "video").validate()
            return value


class TopCategorySerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    category_name = serializers.CharField()
    category_cover = serializers.SerializerMethodField()
    category_cover_mobile = serializers.SerializerMethodField()
    category_cover_homepage = serializers.SerializerMethodField()
    total_sales = serializers.IntegerField()

    def get_category_cover(self, obj):
        category = Category.objects.get(id=obj["category_id"])
        return category.cover.url

    def get_category_cover_mobile(self, obj):
        category = Category.objects.get(id=obj["category_id"])
        return category.cover_mobile.url

    def get_category_cover_homepage(self, obj):
        category = Category.objects.get(id=obj["category_id"])
        return category.cover_homepage.url


class TopBrandSerializer(serializers.Serializer):
    brand_id = serializers.UUIDField()
    brand_name = serializers.CharField()
    brand_logo = serializers.SerializerMethodField()
    brand_cover = serializers.SerializerMethodField()
    brand_cover_mobile = serializers.SerializerMethodField()
    brand_cover_homepage = serializers.SerializerMethodField()
    total_sales = serializers.IntegerField()

    def get_brand_logo(self, obj):
        brand = Brand.objects.get(id=obj["brand_id"])
        return brand.logo.url

    def get_brand_cover(self, obj):
        brand = Brand.objects.get(id=obj["brand_id"])
        return brand.cover.url

    def get_brand_cover_mobile(self, obj):
        brand = Brand.objects.get(id=obj["brand_id"])
        return brand.cover_mobile.url

    def get_brand_cover_homepage(self, obj):
        brand = Brand.objects.get(id=obj["brand_id"])
        return brand.cover_homepage.url
