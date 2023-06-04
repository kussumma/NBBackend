from rest_framework import filters
from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.cart.models import Cart, CartItem
from apps.coupons.models import Coupon, CouponUser
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # get cart items
        user = self.request.user
        cart = Cart.objects.get(user=user)
        try:
            cart_items = CartItem.objects.filter(cart=cart, is_selected=True)
        except CartItem.DoesNotExist:
            raise serializers.ValidationError('Cart is empty')

        # get the coupon
        try:
            coupon_id = self.request.data['coupon']
            coupon = Coupon.objects.get(id=coupon_id)
        except (KeyError, Coupon.DoesNotExist):
            coupon = None

        # check if coupon is already used
        if coupon:
            try:
                CouponUser.objects.get(coupon=coupon, user=user)
                raise serializers.ValidationError('Coupon is already used')
            except CouponUser.DoesNotExist:
                pass
            
            # check if coupon is valid
            if coupon.is_valid() is False:
                raise serializers.ValidationError('Coupon is not valid or expired')

        # calculate total price
        total_price = 0
        for cart_item in cart_items:
            total_price += cart_item.total_price

        # check if coupon is valid for this order
        if coupon:
            if coupon.min_purchase > total_price:
                raise serializers.ValidationError('Total purchase must be higher than minimum purchase required for this coupon')
            
            # calculate discount price
            total_price -= (( coupon.discount_value * total_price ) / 100)

        # create order
        order = serializer.save(user=user, coupon=coupon, final_price=total_price)

        # create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                stock=cart_item.stock,
                quantity=cart_item.quantity,
                total_price=cart_item.total_price,
            )

        # recalculating stock
        for cart_item in cart_items:
            cart_item.stock.quantity -= cart_item.quantity
            cart_item.stock.save()

        # delete cart items
        cart_items.delete()

        # set coupon as used
        if coupon:
            CouponUser.objects.create(coupon=coupon, user=user)

        return order
    
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'coupon__code']
    ordering_fields = ['user', 'coupon', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
