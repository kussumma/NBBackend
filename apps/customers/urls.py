from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteViewset,
    ComplaintViewset,
    ProductRequestViewset,
    FeatureRequestViewset,
    BugReportViewset,
)

router = DefaultRouter()

router.register("favorite", FavoriteViewset, basename="favorite")
router.register("complaint", ComplaintViewset, basename="complaint")
router.register("product-request", ProductRequestViewset, basename="product-request")
router.register("feature-request", FeatureRequestViewset, basename="feature-request")
router.register("bug-report", BugReportViewset, basename="bug-report")

urlpatterns = [
    path("v1/", include(router.urls)),
]
