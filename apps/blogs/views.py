from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import BlogCategory, BlogTag, Blog, BlogImage, BlogVideo, BlogComment
from .serializers import (
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogSerializer,
    BlogImageSerializer,
    BlogVideoSerializer,
    BlogCommentSerializer,
)

from tools.custom_permissions import IsAdminOrReadOnly

User = get_user_model()


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "description"]
    lookup_field = "slug"


class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    lookup_field = "slug"


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "description"]
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        queryset = Blog.objects.all()
        blog = get_object_or_404(queryset, slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogImageViewSet(viewsets.ModelViewSet):
    queryset = BlogImage.objects.all()
    serializer_class = BlogImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["blog__title"]


class BlogVideoViewSet(viewsets.ModelViewSet):
    queryset = BlogVideo.objects.all()
    serializer_class = BlogVideoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["blog__title"]


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["blog__title"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = BlogComment.objects.all()
        blog = self.request.query_params.get("blog", None)
        if blog is not None:
            queryset = queryset.filter(blog__slug=blog)
        return queryset

    def retrieve(self, request, pk=None):
        # get the comment
        queryset = BlogComment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = BlogCommentSerializer(comment)

        # get the replies using the parent comment
        replies = comment.replies.all()
        replies_serializer = BlogCommentSerializer(replies, many=True)

        # return the comment and the replies
        return Response(
            {"comment": serializer.data, "replies": replies_serializer.data}
        )
