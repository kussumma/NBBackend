from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShippingViewSet,
    ShippingRouteViewSet,
    ShippingTariffAPIView,
    ShippingStatusAPIView,
    ShippingTypeViewSet,
    ShippingGroupViewSet,
    ShippingGroupItemViewSet,
    ShippingGroupTariffViewSet,
    ShippingNotificationAPIView,
)

router = DefaultRouter()
router.register("shipping", ShippingViewSet, basename="shipping")
router.register("shipping-route", ShippingRouteViewSet, basename="shipping-route")
router.register("shipping-type", ShippingTypeViewSet, basename="shipping-type")
router.register("shipping-group", ShippingGroupViewSet, basename="shipping-group")
router.register(
    "shipping-group-item", ShippingGroupItemViewSet, basename="shipping-group-item"
)
router.register(
    "shipping-group-tariff",
    ShippingGroupTariffViewSet,
    basename="shipping-group-tariff",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/tariff/", ShippingTariffAPIView.as_view(), name="shipping-tariff"),
    path(
        "v1/shipping-status/", ShippingStatusAPIView.as_view(), name="shipping-status"
    ),
    path(
        "v1/shipping-notification/3311fbbf34dc583d66143c0d91811612049bfa6d9c3fb189e39886e970a01ce336be0d90a04d78963a1a104f029103d6f/",
        ShippingNotificationAPIView.as_view(),
        name="shipping-notification",
    ),
]
