from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShippingViewSet, ShippingTypeViewSet, ShippingRouteViewSet, ShippingRoutePerTypeViewSet, ShippingCommodityViewSet

router = DefaultRouter()
router.register('shipping', ShippingViewSet, basename='shipping')
router.register('shipping-type', ShippingTypeViewSet, basename='shipping-type')
router.register('shipping-route', ShippingRouteViewSet, basename='shipping-route')
router.register('shipping-route-per-type', ShippingRoutePerTypeViewSet, basename='shipping-route-per-type')
router.register('shipping-commodity', ShippingCommodityViewSet, basename='shipping-commodity')

urlpatterns = [
    path('v1/', include(router.urls)),
]