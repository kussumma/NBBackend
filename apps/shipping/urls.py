from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShippingViewSet

router = DefaultRouter()
router.register('shipping', ShippingViewSet, basename='shipping')

urlpatterns = [
    path('v1/', include(router.urls)),
]