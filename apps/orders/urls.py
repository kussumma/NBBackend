from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrderCreateView, OrderListView, OrderDetailView, 
    ReturnOrderViewset, RefundOrderViewset
)

router = DefaultRouter()
router.register('return-order', ReturnOrderViewset, basename='return-order')
router.register('refund-order', RefundOrderViewset, basename='refund-order')

urlpatterns = [
    path('v1/order/create/', OrderCreateView.as_view(), name='order-create'),
    path('v1/order/list/', OrderListView.as_view(), name='order-list'),
    path('v1/order/detail/<uuid:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('v1/order/', include(router.urls)),
]