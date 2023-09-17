from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShippingViewSet, 
    ShippingRouteViewSet,
    ShippingTariffAPIView
)

router = DefaultRouter()
router.register('shipping', ShippingViewSet, basename='shipping')
router.register('shipping-route', ShippingRouteViewSet, basename='shipping-route')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/tariff/', ShippingTariffAPIView.as_view(), name='shipping-tariff'),
]