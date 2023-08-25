from rest_framework import viewsets, permissions, filters

from .models import Shipping, ShippingRoute, ShippingType, ShippingRoutePerType, ShippingCommodity
from .serializers import (
    ShippingSerializer, 
    ShippingWriteSerializer, 
    ShippingRouteSerializer, 
    ShippingTypeSerializer, 
    ShippingRoutePerTypeSerializer, 
    ShippingCommoditySerializer
)

class ShippingTypeViewSet(viewsets.ModelViewSet):
    queryset = ShippingType.objects.all()
    serializer_class = ShippingTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']

class ShippingRouteViewSet(viewsets.ModelViewSet):
    queryset = ShippingRoute.objects.all()
    serializer_class = ShippingRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['city', 'route']
    ordering_fields = ['city', 'route', 'created_at', 'updated_at']
    ordering = ['city', 'route', 'created_at', 'updated_at']

class ShippingRoutePerTypeViewSet(viewsets.ModelViewSet):
    queryset = ShippingRoutePerType.objects.all()
    serializer_class = ShippingRoutePerTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['shipping_type', 'origin_city', 'destination_city']
    ordering_fields = ['shipping_type', 'origin_city', 'destination_city', 'created_at', 'updated_at']
    ordering = ['shipping_type', 'origin_city', 'destination_city', 'created_at', 'updated_at']

class ShippingCommodityViewSet(viewsets.ModelViewSet):
    queryset = ShippingCommodity.objects.all()
    serializer_class = ShippingCommoditySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name']
    ordering_fields = ['code', 'name', 'created_at', 'updated_at']
    ordering = ['code', 'name', 'created_at', 'updated_at']

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['receiver_name', 'receiver_phone', 'receiver_address', 'origin__city', 'destination__city']
    ordering_fields = ['origin__city', 'origin__route', 'destination__city', 'destination__route', 'created_at', 'updated_at']
    ordering = ['origin__city', 'origin__route', 'destination__city', 'destination__route', 'created_at', 'updated_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return ShippingWriteSerializer
        return ShippingSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)