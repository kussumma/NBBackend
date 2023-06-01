from rest_framework import viewsets
from rest_framework import filters
from apps.products.permissions import IsAdminOrReadOnly


from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'ref_code']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order__user__email', 'order__ref_code', 'product__slug']
    ordering_fields = ['created_at']
    ordering = ['-created_at']