from dis import disco
from rest_framework import filters, serializers, viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
import math

from apps.cart.models import Cart, CartItem
from apps.coupons.models import Coupon, CouponUser
from .models import Order, OrderItem, ReturnOrder, RefundOrder, OrderShipping
from .serializers import OrderSerializer, ReturnOrderSerializer, RefundOrderSerializer
from apps.shipping.models import Shipping, ShippingType

from apps.shipping.helpers import lionparcel_original_tariff
from apps.shipping.helpers import lionparcel_tariff_mapping
from .helpers import lionparcel_booking
from .helpers import send_order_confirmation_email


class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "ref_code"]
    ordering_fields = ["user__email", "ref_code", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        # get cart items
        user = self.request.user
        cart = Cart.objects.get(user=user)

        cart_items = CartItem.objects.filter(cart=cart, is_selected=True)
        if not cart_items:
            return Response(
                {"error": "No item found in the cart"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # calculate subtotal amount and total weight
        subtotal_amount = 0
        total_discount = 0
        total_paid = 0
        total_weight = 0

        for cart_item in cart_items:
            subtotal_amount += cart_item.total_price
            total_weight += cart_item.stock.weight * cart_item.quantity

        # set total paid
        total_paid += subtotal_amount

        # convert to kg
        if total_weight > 0:
            total_weight = math.ceil(total_weight / 1000)

        # get the coupon
        coupon_code_input = request.data.get("coupon")
        coupon_code_input2 = request.data.get("coupon2")

        # Get the first coupon
        if coupon_code_input:
            coupon_prefix = coupon_code_input[:8]
            coupon_code = coupon_code_input[8:]

            try:
                coupon = Coupon.objects.get(prefix_code=coupon_prefix)
            except Coupon.DoesNotExist:
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            if not coupon.is_verified(coupon_code) or not coupon.is_valid():
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                coupon_user = CouponUser.objects.get(coupon=coupon, user=user)
            except CouponUser.DoesNotExist:
                coupon_user = None

            if coupon.is_limited and coupon_user:
                return Response(
                    {"error": "Coupon is already used"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the coupon is valid for this order and calculate discount
            if not coupon.is_private and coupon.min_purchase > subtotal_amount:
                raise serializers.ValidationError(
                    "Total purchase must be higher than minimum purchase allowed for the first coupon"
                )
        else:
            coupon = None

        # Get the second coupon
        if coupon_code_input2:
            coupon_prefix2 = coupon_code_input2[:8]
            coupon_code2 = coupon_code_input2[8:]

            try:
                coupon2 = Coupon.objects.get(prefix_code=coupon_prefix2)
            except Coupon.DoesNotExist:
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            if not coupon2.is_verified(coupon_code2) or not coupon2.is_valid():
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                coupon_user2 = CouponUser.objects.get(coupon=coupon2, user=user)
            except CouponUser.DoesNotExist:
                coupon_user2 = None

            if coupon2.is_limited and coupon_user2:
                return Response(
                    {"error": "Coupon is already used"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the second coupon is valid for this order and calculate discount
            if not coupon2.is_private and coupon2.min_purchase > subtotal_amount:
                raise serializers.ValidationError(
                    "Total purchase must be higher than the minimum purchase allowed for the second coupon"
                )
        else:
            coupon2 = None

        # Check if both coupons are public, or prioritize the private coupon
        if coupon and coupon2:
            if not coupon.is_private and not coupon2.is_private:
                return Response(
                    {"error": "Only one free coupon is allowed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif coupon.id == coupon2.id:
                return Response(
                    {"error": "Coupon can't be used twice"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif not coupon.is_private and coupon2.is_private:
                coupon, coupon2 = (
                    coupon2,
                    coupon,
                )  # Swap the coupons to prioritize the private one

        if coupon:
            if coupon.is_private:
                total_discount += coupon.max_purchase
                total_paid -= coupon.max_purchase
            else:
                total_discount += (coupon.discount_value * subtotal_amount) / 100
                total_paid -= (coupon.discount_value * subtotal_amount) / 100

        if coupon2:
            if coupon2.is_private:
                total_discount += coupon2.max_purchase
                total_paid -= coupon2.max_purchase
            else:
                total_discount += (coupon2.discount_value * subtotal_amount) / 100
                total_paid -= (coupon2.discount_value * subtotal_amount) / 100

        if total_discount > subtotal_amount:
            total_discount = subtotal_amount
            total_paid = 0

        # get shipping details
        try:
            shipping = Shipping.objects.get(user=user, is_default=True)
        except Shipping.DoesNotExist:
            return Response(
                {"error": "Default shipping is not set"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # get shipping type
        shipping_type = request.data.get("shipping_type")
        try:
            registered_shipping_type = ShippingType.objects.get(code=shipping_type)
        except ShippingType.DoesNotExist:
            return Response(
                {"error": "Shipping type is not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            original_tariff = lionparcel_original_tariff(total_weight, shipping)
            if isinstance(original_tariff, Response):
                return original_tariff
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = lionparcel_tariff_mapping(original_tariff)
            if isinstance(response, Response):
                return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # shipping cost & estimation
        shipping_type = None
        shipping_type_name = None
        shipping_cost = 0
        shipping_estimation = None

        # search the shipping type in response list
        for item in response:
            if item.get("shipping_type") == registered_shipping_type.code:
                shipping_type = item.get("shipping_type")
                shipping_type_name = item.get("shipping_type_name")
                shipping_cost = item.get("total_tariff")
                shipping_estimation = item.get("estimasi_sla")

        # calculate tax amount
        # tax_amount = math.ceil(((subtotal_amount + shipping_cost) * 10) / 100)
        tax_amount = 0

        # calculate total price
        total_amount = total_paid + shipping_cost + tax_amount

        # use transaction atomic when creating order
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            order = serializer.save(
                user=user,
                coupon=coupon_code_input,
                coupon2=coupon_code_input2,
                tax_amount=tax_amount,
                shipping_amount=shipping_cost,
                subtotal_amount=subtotal_amount,
                total_amount=math.ceil(total_amount),
                total_weight=math.ceil(total_weight),
                discount_amount=math.ceil(total_discount),
            )

        # create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                quantity=cart_item.quantity,
                product=cart_item.product,
                product_name=cart_item.product.name,
                stock=cart_item.stock,
                stock_discount=cart_item.stock.discount,
                stock_sku=cart_item.stock.sku,
                stock_price=cart_item.stock.price,
                product_cover=cart_item.product.cover,
                stock_size=cart_item.stock.size,
                stock_color=cart_item.stock.color,
                stock_color_code=cart_item.stock.color_code,
                stock_variant=cart_item.stock.variant,
                stock_weight=cart_item.stock.weight,
                stock_length=cart_item.stock.length,
                stock_width=cart_item.stock.width,
                stock_height=cart_item.stock.height,
            )

        # recalculating stock
        for cart_item in cart_items:
            cart_item.stock.quantity -= cart_item.quantity
            cart_item.stock.save()

        # delete cart items
        cart_items.delete()

        # set coupon as used
        if coupon and coupon.is_limited:
            CouponUser.objects.create(coupon=coupon, user=user)

        if coupon2 and coupon2.is_limited:
            CouponUser.objects.create(coupon=coupon2, user=user)

        # create shipping order
        OrderShipping.objects.create(
            order=order,
            shipping=shipping,
            receiver_name=shipping.receiver_name,
            receiver_phone=shipping.receiver_phone,
            receiver_address=shipping.receiver_address,
            destination_route=shipping.destination.route,
            shipping_type=shipping_type,
            shipping_type_name=shipping_type_name,
            shipping_estimation=shipping_estimation,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReturnOrderViewset(viewsets.ModelViewSet):
    serializer_class = ReturnOrderSerializer
    queryset = ReturnOrder.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["order__user__email", "order__ref_code", "status"]
    ordering_fields = ["order__user", "order__ref_code", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return ReturnOrder.objects.filter(order__user=user)

    def create(self, request, *args, **kwargs):
        # get order
        order_id = request.data.get("order")
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # check if order is already returned
        try:
            ReturnOrder.objects.get(order=order)
            raise serializers.ValidationError("Order is already returned")
        except ReturnOrder.DoesNotExist:
            pass

        # create return order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order)


class RefundOrderViewset(viewsets.ModelViewSet):
    serializer_class = RefundOrderSerializer
    queryset = RefundOrder.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["order__user__email", "order__ref_code", "status"]
    ordering_fields = ["order__user", "order__ref_code", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return RefundOrder.objects.filter(order__user=user)

    def create(self, request, *args, **kwargs):
        # get order
        order_id = request.data.get("order")
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # check if order is already refunded
        try:
            RefundOrder.objects.get(order=order)
            raise serializers.ValidationError("Order is already refunded")
        except RefundOrder.DoesNotExist:
            pass

        # create refund order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order)


class ConfirmOrderAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get("pk")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # send email to user
        try:
            send_order_confirmation_email(order_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # update order status
        order.status = "confirmed"
        order.save()

        return Response({"success": "Order is confirmed"}, status=status.HTTP_200_OK)


class BookShipmentAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get("pk")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # booking shipment
        try:
            lionparcel_booking(order_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # update order status
        order.status = "shipping"
        order.save()

        return Response({"success": "Order is shipped"}, status=status.HTTP_200_OK)


class CouponCheckingAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Check if the coupon is valid for the order and calculate the discount
        This API requires one or two coupon codes and returns the total discount
        """
        # get cart items
        user = self.request.user
        cart = Cart.objects.get(user=user)

        cart_items = CartItem.objects.filter(cart=cart, is_selected=True)
        if not cart_items:
            return Response(
                {"error": "No item found in the cart"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # calculate subtotal amount
        subtotal_amount = 0
        total_discount = 0
        total_paid = 0

        for cart_item in cart_items:
            subtotal_amount += cart_item.total_price

        # set total paid
        total_paid += subtotal_amount

        # get the coupon
        coupon_code_input = request.GET.get("coupon")
        coupon_code_input2 = request.GET.get("coupon2")

        # Get the first coupon
        if coupon_code_input:
            coupon_prefix = coupon_code_input[:8]
            coupon_code = coupon_code_input[8:]

            try:
                coupon = Coupon.objects.get(prefix_code=coupon_prefix)
            except Coupon.DoesNotExist:
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            if not coupon.is_verified(coupon_code) or not coupon.is_valid():
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                coupon_user = CouponUser.objects.get(coupon=coupon, user=user)
            except CouponUser.DoesNotExist:
                coupon_user = None

            if coupon.is_limited and coupon_user:
                return Response(
                    {"error": "Coupon is already used"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the coupon is valid for this order and calculate discount
            if not coupon.is_private and coupon.min_purchase > subtotal_amount:
                raise serializers.ValidationError(
                    "Total purchase must be higher than minimum purchase allowed for the first coupon"
                )
        else:
            coupon = None

        # Get the second coupon
        if coupon_code_input2:
            coupon_prefix2 = coupon_code_input2[:8]
            coupon_code2 = coupon_code_input2[8:]

            try:
                coupon2 = Coupon.objects.get(prefix_code=coupon_prefix2)
            except Coupon.DoesNotExist:
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            if not coupon2.is_verified(coupon_code2) or not coupon2.is_valid():
                return Response(
                    {"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                coupon_user2 = CouponUser.objects.get(coupon=coupon2, user=user)
            except CouponUser.DoesNotExist:
                coupon_user2 = None

            if coupon2.is_limited and coupon_user2:
                return Response(
                    {"error": "Coupon is already used"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the second coupon is valid for this order and calculate discount
            if not coupon2.is_private and coupon2.min_purchase > subtotal_amount:
                raise serializers.ValidationError(
                    "Total purchase must be higher than the minimum purchase allowed for the second coupon"
                )
        else:
            coupon2 = None

        # Check if both coupons are public, or prioritize the private coupon
        if coupon and coupon2:
            if not coupon.is_private and not coupon2.is_private:
                return Response(
                    {"error": "Only one free coupon is allowed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif coupon.id == coupon2.id:
                return Response(
                    {"error": "Coupon can't be used twice"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif not coupon.is_private and coupon2.is_private:
                coupon, coupon2 = (
                    coupon2,
                    coupon,
                )  # Swap the coupons to prioritize the private one

        if coupon:
            if coupon.is_private:
                total_discount += coupon.max_purchase
                total_paid -= coupon.max_purchase
            else:
                total_discount += (coupon.discount_value * subtotal_amount) / 100
                total_paid -= (coupon.discount_value * subtotal_amount) / 100

        if coupon2:
            if coupon2.is_private:
                total_discount += coupon2.max_purchase
                total_paid -= coupon2.max_purchase
            else:
                total_discount += (coupon2.discount_value * subtotal_amount) / 100
                total_paid -= (coupon2.discount_value * subtotal_amount) / 100

        if total_discount > subtotal_amount:
            total_discount = subtotal_amount
            total_paid = 0

        discount_percentage = 0
        if subtotal_amount > 0:
            discount_percentage = math.ceil((total_discount / subtotal_amount) * 100)

        return Response(
            {
                "subtotal_amount": subtotal_amount,
                "total_discount": total_discount,
                "dicount_percentage": discount_percentage,
                "total_paid": total_paid,
            },
            status=status.HTTP_200_OK,
        )
