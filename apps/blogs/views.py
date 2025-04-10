from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import (
    BlogCategory,
    BlogTag,
    Blog,
    BlogImage,
    BlogVideo,
    BlogComment,
    BlogUrl,
)
from .serializers import (
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogSerializer,
    BlogImageSerializer,
    BlogVideoSerializer,
    BlogCommentSerializer,
    BlogUrlSerializer,
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
    ordering = ["name"]
    lookup_field = "slug"


class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    lookup_field = "slug"


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = {
        "category": ["exact"],
        "tags": ["exact"],
        "is_published": ["exact"],
        "is_featured": ["exact"],
        "is_headline": ["exact"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["title", "content"]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        return queryset

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
    ordering = ["-created_at"]


class BlogVideoViewSet(viewsets.ModelViewSet):
    queryset = BlogVideo.objects.all()
    serializer_class = BlogVideoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["blog__title"]
    ordering = ["-created_at"]


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["blog__title"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = BlogComment.objects.all()
        blog = self.request.GET.get("blog", None)
        if blog is not None:
            queryset = queryset.filter(blog__slug=blog)
        return queryset

    def retrieve(self, request, pk=None):
        # get the comment
        queryset = BlogComment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = BlogCommentSerializer(comment)

        # get the replies using the parent comment
        replies = queryset.filter(parent_comment=comment)
        replies_serializer = BlogCommentSerializer(replies, many=True)

        # return the comment and the replies
        return Response(
            {"comment": serializer.data, "replies": replies_serializer.data}
        )


class BlogUrlViewSet(viewsets.ModelViewSet):
    queryset = BlogUrl.objects.all()
    serializer_class = BlogUrlSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["blog__title"]
    ordering = ["-created_at"]
