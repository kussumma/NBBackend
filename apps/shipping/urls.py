from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShippingViewSet,
    ShippingRouteViewSet,
    ShippingTariffAPIView,
    ShippingTypeViewSet,
    ShippingGroupViewSet,
    ShippingGroupItemViewSet,
    ShippingGroupTariffViewSet,
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
]
