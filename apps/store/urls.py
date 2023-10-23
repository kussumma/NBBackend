from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ContactViewSet,
    AboutViewSet,
    PartnerViewSet,
    InvestorViewSet,
    PolicyViewSet,
    FAQViewSet,
    CopyRightViewSet,
)

router = DefaultRouter()
router.register("contact", ContactViewSet)
router.register("about", AboutViewSet)
router.register("partner", PartnerViewSet)
router.register("investor", InvestorViewSet)
router.register("policy", PolicyViewSet)
router.register("faq", FAQViewSet)
router.register("copy_right", CopyRightViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
