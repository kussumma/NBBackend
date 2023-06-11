from rest_framework import viewsets, permissions, filters

from .models import Shipping
from .serializers import ShippingSerializer

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'village', 'district', 'city', 'province', 'country', 'zip_code', 'phone_number', 'shipping_service']
    ordering_fields = ['name', 'address', 'village', 'district', 'city', 'province', 'country', 'zip_code', 'phone_number', 'shipping_service']
    ordering = ['name', 'address']

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(order__user=self.request.user)
