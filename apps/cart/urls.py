from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CartViewSet,
    CartItemViewSet
)

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('cart-item', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('v1/', include(router.urls)),
]