from rest_framework import viewsets, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['user__email']
    filterset_fields = {
        'user': ['exact'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['user', 'created_at', 'updated_at']
    ordering = ['-created_at']
    lookup_field = 'user'

    def get_cart_data(self, cart):
        # get cart items
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)

        # count total items
        total_items = sum([item.quantity for item in cart_items])

        # count total price
        total_price = sum([item.total_price for item in cart_items])

        return {
            'cart': self.get_serializer(cart).data,
            'cart_items': cart_items_serializer.data,
            'total_items': total_items,
            'total_price': total_price,
        }

    def list(self, request, *args, **kwargs):
        # get user
        user = self.request.user

        # get cart
        cart = get_object_or_404(Cart, user=user)

        return Response(self.get_cart_data(cart))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(self.get_cart_data(instance))
    
    def get_queryset(self):
        queryset = Cart.objects.all()
        user = self.request.user
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
    }
    ordering_fields = ['cart', 'product', 'stock', 'quantity', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = CartItem.objects.all()
        cart = get_object_or_404(Cart, user=self.request.user)

        if cart is not None:
            queryset = queryset.filter(cart=cart)
        return queryset
    
    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        stock = request.data.get('stock', None)
        quantity = request.data.get('quantity', 1)

        try:
            # Check if the product is already in the cart
            cart_item = CartItem.objects.filter(cart=cart, stock=stock).first()
            if cart_item is not None:
                cart_item.increase_quantity(quantity)
                serializer = self.get_serializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(cart=cart)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response({
                'message': 'Stock is not valid',
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        increase_quantity = request.data.get('increase_quantity', False)
        decrease_quantity = request.data.get('decrease_quantity', False)
        set_as_selected = request.data.get('set_as_selected', False)

        if increase_quantity:
            # Check if the quantity of this product is enough
            if instance.quantity < instance.stock.quantity:
                instance.increase_quantity()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({
                    'message': 'Sorry, this product has not enough stock',
                    'quantity': instance.quantity,
                }, status=status.HTTP_400_BAD_REQUEST)

        elif decrease_quantity:
            # Check if the item quantity is more than 1
            if instance.quantity > 1:
                instance.decrease_quantity()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({
                    'message': 'Sorry, the quantity of this product has reached the minimum.',
                    'quantity': instance.quantity,
                }, status=status.HTTP_400_BAD_REQUEST)
            
        elif set_as_selected:
            # Set this item as selected
            instance.set_as_selected()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return super().partial_update(request, *args, **kwargs)

class SelectedItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart, is_selected=True)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)