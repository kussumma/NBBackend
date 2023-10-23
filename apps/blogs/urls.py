from django.urls import path, include
from rest_framework import routers

from .views import (
    BlogCategoryViewSet,
    BlogTagViewSet,
    BlogViewSet,
    BlogImageViewSet,
    BlogVideoViewSet,
    BlogCommentViewSet,
    BlogUrlViewSet,
)

router = routers.DefaultRouter()
router.register("blog-categories", BlogCategoryViewSet)
router.register("blog-tags", BlogTagViewSet)
router.register("blogs", BlogViewSet)
router.register("blog-images", BlogImageViewSet)
router.register("blog-videos", BlogVideoViewSet)
router.register("blog-comments", BlogCommentViewSet)
router.register("blog-urls", BlogUrlViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
