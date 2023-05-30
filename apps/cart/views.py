from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__email']
    filterset_fields = {
        'user': ['exact'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['user', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get cart items
        cart_items = CartItem.objects.filter(cart=instance)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)

        # count total items
        total_items = sum([item.quantity for item in cart_items])

        # count total price
        total_price = sum([item.price for item in cart_items])

        return Response({
            'cart': serializer.data,
            'cart_items': cart_items_serializer.data,
            'total_items': total_items,
            'total_price': total_price,
        })
    
    def get_queryset(self):
        queryset = Cart.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['cart__user__email', 'product__name']
    filterset_fields = {
        'cart': ['exact'],
        'product': ['exact'],
        'stock': ['exact'],
        'quantity': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte'],
        'is_active': ['exact'],
    }
    ordering_fields = ['cart', 'product', 'stock', 'quantity', 'created_at', 'is_active']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = CartItem.objects.all()
        cart = self.request.query_params.get('cart', None)
        if cart is not None:
            queryset = queryset.filter(cart=cart)
        return queryset
