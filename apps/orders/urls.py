from django.urls import path, include

from .views import OrderCreateView, OrderListView, OrderDetailView

urlpatterns = [
    path('v1/order/create/', OrderCreateView.as_view(), name='order-create'),
    path('v1/order/list/', OrderListView.as_view(), name='order-list'),
    path('v1/order/detail/<uuid:id>/', OrderDetailView.as_view(), name='order-detail'),
]