from django.shortcuts import redirect
from django.contrib import messages

from apps.orders.models import Order

from .helpers import (
    send_order_confirmation_email,
    lionparcel_booking,
    send_order_shipping_email,
)


def confirm_order_view(request, pk):
    if request.user.is_superuser:
        try:
            order = Order.objects.get(pk=pk)
            if order.payment_status == "settlement":
                send_order_confirmation_email(order.id)
                order.status = "confirmed"
                order.save()
                messages.success(
                    request,
                    f"Order with ID {order.ref_code} is confirmed successfully.",
                )
            else:
                messages.error(
                    request,
                    f"Order with ID {order.ref_code} is not confirmed because payment status is not settlement.",
                )
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "You are not authorized to do this action")

    return redirect("admin:orders_order_changelist")


def book_shipment_view(request, pk):
    if request.user.is_superuser:
        try:
            order = Order.objects.get(pk=pk)
            if order.status == "confirmed":
                lionparcel_booking(order.id)
                send_order_shipping_email(order.id)
                order.status = "shipping"
                order.save()
                messages.success(
                    request, f"Order with ID {order.ref_code} is shipped successfully."
                )
            else:
                messages.error(
                    request,
                    f"Order with ID {order.ref_code} is not shipped because status is not confirmed.",
                )
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "You are not authorized to do this action")

    return redirect("admin:orders_order_changelist")
