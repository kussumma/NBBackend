from rest_framework import filters
from rest_framework import generics, viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.cart.models import Cart, CartItem
from apps.coupons.models import Coupon, CouponUser
from .models import Order, OrderItem, ReturnOrder, RefundOrder, ReturnImage
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
        except CartItem.DoesNotExist:
            cart_items = None

        # check if cart is empty
        if cart_items is None or len(cart_items) == 0:
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

        # calculate subtotal amount
        subtotal_amount = 0
        for cart_item in cart_items:
            subtotal_amount += cart_item.total_price

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
            shipping = None

        # calculate shipping cost
        if shipping:
            contact = Contact.objects.first()

            lionparcel = LionParcelHelper(LIONPARCEL_API_KEY)

            try:
                shipping_cost = lionparcel.make_booking(
                    stt_goods_estimate_price=subtotal_amount, 
                    stt_origin=contact.origin,
                    stt_destination=shipping.destination,
                    stt_sender_name=contact.name,
                    stt_sender_phone=contact.phone,
                    stt_sender_address=contact.address,
                    stt_recipient_name=shipping.name,
                    stt_recipient_address=shipping.address, 
                    stt_recipient_phone=shipping.phone,
                    stt_product_type=shipping.product_type,
                    stt_pieces=[
                        {
                            'weight': shipping.weight,
                            'length': shipping.length,
                            'width': shipping.width,
                            'height': shipping.height,
                            'quantity': 1
                        },
                    ]
                )
            except Exception as e:
                print(e)

        else:
            shipping_cost = 0
            shipping_ref_code = None

        # calculate tax amount
        tax_amount = 0

        # calculate total price
        total_amount = subtotal_amount + shipping_cost + tax_amount

        # get payment status
        try:
            payment_status = self.request.data['payment_status']
        except KeyError:
            payment_status = 'pending'

        # get payment ref code
        try:
            payment_ref_code = self.request.data['payment_ref_code']
        except KeyError:
            payment_ref_code = None

        # get note
        try:
            note = self.request.data['note']
        except KeyError:
            note = None

        # create order
        order = serializer.save(
            user=user, 
            coupon=coupon, 
            shipping=shipping, 
            shipping_cost=shipping_cost, 
            shipping_ref_code=shipping_ref_code,
            tax_amount = tax_amount,
            subtotal_amount=subtotal_amount,
            total_amount=total_amount,
            payment_status=payment_status,
            payment_ref_code=payment_ref_code,
            note=note
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
