from rest_framework import viewsets, permissions, filters, views, status
from rest_framework.response import Response

from .models import Shipping, ShippingRoute
from .serializers import (
    ShippingSerializer, 
    ShippingWriteSerializer, 
    ShippingRouteSerializer, 
)
from tools.lionparcel_helper import LionParcelHelper
from system.settings import LIONPARCEL_API_KEY
from apps.store.models import Contact
from apps.cart.models import Cart, CartItem

class ShippingRouteViewSet(viewsets.ModelViewSet):
    queryset = ShippingRoute.objects.all()
    serializer_class = ShippingRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['city', 'route']
    ordering_fields = ['city', 'route', 'created_at', 'updated_at']
    ordering = ['city', 'route', 'created_at', 'updated_at']

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

class ShippingTariffAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # get cart items
        user = self.request.user
        cart = Cart.objects.get(user=user)
        
        try:
            cart_items = CartItem.objects.filter(cart=cart, is_selected=True)
        except CartItem.DoesNotExist:
            cart_items = None

        if not cart_items:
            return Response({"error": "cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # get shipping
        shipping = request.GET.get('shipping')

        if not shipping:
            return Response({"error": "shipping is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            shipping = Shipping.objects.get(id=shipping)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # get store contact
        try:
            store = Contact.objects.get(is_active=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        weight = 0

        for cart_item in cart_items:
            weight += cart_item.stock.weight * cart_item.quantity

        lionparcel = LionParcelHelper(LIONPARCEL_API_KEY)
        try:
            response = lionparcel.get_tariff(
                origin=store.origin,
                destination=shipping.destination.route,
                weight=weight,
                commodity=store.commodity,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)
