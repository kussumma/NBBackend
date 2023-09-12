from rest_framework import filters
from rest_framework import generics, viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
import math

from apps.cart.models import Cart, CartItem
from apps.coupons.models import Coupon, CouponUser
from .models import Order, OrderItem, ReturnOrder, RefundOrder
from .serializers import OrderSerializer, ReturnOrderSerializer, RefundOrderSerializer
from apps.shipping.models import Shipping
from tools.lionparcel_helper import LionParcelHelper
from system.settings import LIONPARCEL_API_KEY
from apps.store.models import Contact

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
        except (KeyError, CartItem.DoesNotExist):
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
            
        # calculate subtotal amount and total weight
        subtotal_amount = 0
        total_weight = 0
        for cart_item in cart_items:
            subtotal_amount += cart_item.total_price
            total_weight += cart_item.stock.weight * cart_item.quantity

        # check if coupon is valid for this order
        if coupon:
            if coupon.min_purchase > subtotal_amount:
                raise serializers.ValidationError('Total purchase must be higher than minimum purchase required for this coupon')
            
            # calculate discount price
            subtotal_amount -= (( coupon.discount_value * subtotal_amount ) / 100)

        # get shipping details
        try:
            shipping_id = self.request.data['shipping']
            shipping = Shipping.objects.get(id=shipping_id)
        except (KeyError, Shipping.DoesNotExist):
            raise serializers.ValidationError('Shipping is required')
        
        # get shipping cost
        try:
            shipping_cost = self.request.data['shipping_cost']
            shipping_cost = int(shipping_cost)
        except KeyError:
            raise serializers.ValidationError('Shipping cost is required')

        # get shipping type
        try:
            shipping_type = self.request.data['shipping_type']
        except KeyError:
            raise serializers.ValidationError('Shipping type is required')

        # calculate shipping cost
        if shipping:
            contact = Contact.objects.get(is_active=True)

            lionparcel = LionParcelHelper(LIONPARCEL_API_KEY)

            # create stt pieces
            stt_pieces = []
            for cart_item in cart_items:
                stt_pieces.append({
                    'stt_piece_gross_weight': cart_item.stock.weight,
                    'stt_piece_length': cart_item.stock.length,
                    'stt_piece_width': cart_item.stock.width,
                    'stt_piece_height': cart_item.stock.height,
                })

            # create booking data
            booking_data = {
                "stt_goods_estimate_price": 0,
                "stt_origin": contact.origin,
                "stt_destination": shipping.destination.route,
                "stt_sender_name": contact.name,
                "stt_sender_phone": contact.phone,
                "stt_sender_address": contact.address,
                "stt_recipient_name": shipping.receiver_name,
                "stt_recipient_address": shipping.receiver_address,
                "stt_recipient_phone": shipping.receiver_phone,
                "stt_product_type": shipping_type,
                "stt_commodity_code": contact.commodity,
                "stt_pieces": stt_pieces
            }
                
            try:
                booking = lionparcel.make_booking(booking_data)

                # get shipping ref code
                if booking['success']:
                    shipping_ref_code = booking['data']['stt'][0]['stt_no']
                else:
                    raise serializers.ValidationError(booking['message']['en'])
            
            except Exception as e:
                raise serializers.ValidationError(str(e))
                 
        # calculate tax amount
        tax_amount = math.ceil(( subtotal_amount * 10 ) / 100)

        # calculate total price
        total_amount = subtotal_amount + shipping_cost + tax_amount

        # use transaction atomic when creating order
        with transaction.atomic():
            order = serializer.save(
                user=user, 
                coupon=coupon, 
                shipping=shipping, 
                shipping_cost=shipping_cost, 
                shipping_ref_code=shipping_ref_code,
                tax_amount = tax_amount,
                subtotal_amount=subtotal_amount,
                total_amount=math.ceil(total_amount),
                total_weight=math.ceil(total_weight)
            )

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

class ReturnOrderViewset(viewsets.ModelViewSet):
    serializer_class = ReturnOrderSerializer
    queryset = ReturnOrder.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order__user__email', 'order__ref_code', 'status']
    ordering_fields = ['order__user', 'order__ref_code', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return ReturnOrder.objects.filter(order__user=user)
    
    def perform_create(self, serializer):
        # get order
        order_id = self.request.data['order']
        order = Order.objects.get(id=order_id)

        # check if order is already returned
        try:
            ReturnOrder.objects.get(order=order)
            raise serializers.ValidationError('Order is already returned')
        except ReturnOrder.DoesNotExist:
            pass

        # create return order
        serializer.save(order=order)

class RefundOrderViewset(viewsets.ModelViewSet):
    serializer_class = RefundOrderSerializer
    queryset = RefundOrder.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order__user__email', 'order__ref_code', 'status']
    ordering_fields = ['order__user', 'order__ref_code', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return RefundOrder.objects.filter(order__user=user)
    
    def perform_create(self, serializer):
        # get order
        order_id = self.request.data['order']
        order = Order.objects.get(id=order_id)

        # check if order is already refunded
        try:
            RefundOrder.objects.get(order=order)
            raise serializers.ValidationError('Order is already refunded')
        except RefundOrder.DoesNotExist:
            pass

        # create refund order
        serializer.save(order=order)
