from numpy import rec
from rest_framework import viewsets, permissions, filters, views, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from tools.custom_permissions import IsAdminOrReadOnly
import math

from apps.orders.models import Order
from .models import (
    Shipping,
    ShippingRoute,
    ShippingGroup,
    ShippingType,
    ShippingGroupItem,
    ShippingGroupTariff,
)
from .serializers import (
    ShippingSerializer,
    ShippingWriteSerializer,
    ShippingRouteSerializer,
    ShippingGroupItemSerializer,
    ShippingGroupTariffSerializer,
    ShippingTypeSerializer,
    ShippingGroupSerializer,
)
from apps.cart.models import Cart, CartItem
from apps.orders.models import OrderShipping

from .helpers import lionparcel_original_tariff
from .helpers import lionparcel_tariff_mapping
from .helpers import lionparcel_track_status


class ShippingRouteViewSet(viewsets.ModelViewSet):
    queryset = ShippingRoute.objects.all()
    serializer_class = ShippingRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["city", "route"]
    ordering_fields = ["city", "route", "created_at", "updated_at"]
    ordering = ["city", "route", "created_at", "updated_at"]


class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "receiver_name",
        "receiver_phone",
        "receiver_address",
        "origin__city",
        "destination__city",
    ]
    ordering_fields = [
        "destination__city",
        "destination__route",
        "created_at",
        "updated_at",
    ]
    ordering = ["destination__city", "destination__route", "created_at", "updated_at"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return ShippingWriteSerializer
        return ShippingSerializer

    def perform_create(self, serializer):
        # check if the shipping reach the maximum limit
        user = self.request.user
        shipping_count = Shipping.objects.filter(user=user).count()

        if shipping_count >= 5:
            raise ValidationError(
                "Maximum limit reached, you can only have 5 shipping address."
            )

        serializer.save(user=user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        set_as_default = request.data.get("set_as_default", False)
        if set_as_default:
            Shipping.objects.filter(user=instance.user).update(is_default=False)
            instance.is_default = True
            instance.save()
        return super().partial_update(request, *args, **kwargs)


class ShippingTariffAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        # get cart and items
        cart = Cart.objects.get(user=user)

        try:
            cart_items = CartItem.objects.filter(cart=cart, is_selected=True)
        except CartItem.DoesNotExist:
            cart_items = None

        if not cart_items:
            return Response(
                {"error": "cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        weight = 0

        for cart_item in cart_items:
            weight += cart_item.stock.weight * cart_item.quantity

        # convert the weight to kg from gram and round it up
        if weight > 0:
            weight = math.ceil(weight / 1000)

        try:
            shipping = Shipping.objects.get(user=user, is_default=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            original_tariff = lionparcel_original_tariff(weight, shipping)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = lionparcel_tariff_mapping(original_tariff)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)


class ShippingStatusAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        shipping_ref_code = request.data.get("shipping_ref_code")

        try:
            ordershipping = OrderShipping.objects.get(
                shipping_ref_code=shipping_ref_code
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        shipping_ref_code = ordershipping.shipping_ref_code

        try:
            response = lionparcel_track_status(shipping_ref_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)


class ShippingNotificationAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        stt_no = request.data.get("stt_no")
        status_code = request.data.get("status_code")

        if status_code == "POD":
            try:
                order = Order.objects.get(order_shipping__shipping_ref_code=stt_no)
                order.status = "complete"
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "success"}, status=status.HTTP_200_OK)


class ShippingGroupViewSet(viewsets.ModelViewSet):
    queryset = ShippingGroup.objects.all()
    serializer_class = ShippingGroupSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name", "created_at", "updated_at"]


class ShippingGroupItemViewSet(viewsets.ModelViewSet):
    queryset = ShippingGroupItem.objects.all()
    serializer_class = ShippingGroupItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["shipping_group__name", "shipping_route__route"]
    ordering_fields = [
        "shipping_group__name",
        "shipping_route__route",
        "created_at",
        "updated_at",
    ]
    ordering = [
        "shipping_group__name",
        "shipping_route__route",
        "created_at",
        "updated_at",
    ]


class ShippingGroupTariffViewSet(viewsets.ModelViewSet):
    queryset = ShippingGroupTariff.objects.all()
    serializer_class = ShippingGroupTariffSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["shipping_group__name", "shipping_type__name"]
    ordering_fields = [
        "shipping_group__name",
        "shipping_type__name",
        "created_at",
        "updated_at",
    ]
    ordering = [
        "shipping_group__name",
        "shipping_type__name",
        "created_at",
        "updated_at",
    ]


class ShippingTypeViewSet(viewsets.ModelViewSet):
    queryset = ShippingType.objects.all()
    serializer_class = ShippingTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name", "created_at", "updated_at"]
