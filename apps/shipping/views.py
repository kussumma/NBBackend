from rest_framework import viewsets, permissions, filters

from .models import Shipping
from .serializers import ShippingSerializer

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user', 'receiver_name', 'receiver_phone', 'receiver_address', 'origin', 'destination', 'shipping_type']
    ordering_fields = ['origin', 'destination', 'created_at', 'updated_at']
    ordering = ['origin', 'destination', 'created_at', 'updated_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
