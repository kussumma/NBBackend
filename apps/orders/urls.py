from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet)
router.register('order-items', OrderItemViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]