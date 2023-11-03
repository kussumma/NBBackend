from rest_framework import serializers
from tools.fileupload_helper import FileUploadHelper
from .models import (
    BlogCategory,
    BlogTag,
    Blog,
    BlogImage,
    BlogVideo,
    BlogComment,
    BlogUrl,
)


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"
        read_only_fields = ("slug",)

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"
        read_only_fields = ("slug",)


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = "__all__"

    def validate_image(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class BlogVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogVideo
        fields = "__all__"


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "user")


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ("slug", "created_at", "updated_at", "author")

    def validate_cover(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class BlogUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUrl
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )
