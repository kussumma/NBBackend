from rest_framework import serializers

from .models import BlogCategory, BlogTag, Blog, BlogImage, BlogVideo, BlogComment


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"
        read_only_fields = ("slug",)


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"
        read_only_fields = ("slug",)


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = "__all__"


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
