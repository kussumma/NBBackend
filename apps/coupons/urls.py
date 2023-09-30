from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DiscountTypeViewSet,
    CouponViewSet,
    CouponUserViewSet,
    CouponBannerViewSet,
)

router = DefaultRouter()
router.register("discount-types", DiscountTypeViewSet, basename="discount-type")
router.register("coupons", CouponViewSet, basename="coupon")
router.register("coupon-users", CouponUserViewSet, basename="coupon-user")
router.register("coupon-banners", CouponBannerViewSet, basename="coupon-banner")

urlpatterns = [
    path("v1/", include(router.urls)),
]
