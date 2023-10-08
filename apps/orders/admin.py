from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Order,
    OrderItem,
    ReturnOrder,
    ReturnImage,
    RefundOrder,
    OrderShipping,
)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderShippingInline(admin.StackedInline):
    model = OrderShipping
    extra = 0


class ReturnOrderInline(admin.StackedInline):
    model = ReturnOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_filter = ("status", "payment_status", "created_at", "updated_at")
    search_fields = ("ref_code", "user__email", "user__first_name", "user__last_name")
    inlines = [
        OrderItemInline,
        OrderShippingInline,
        ReturnOrderInline,
    ]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                "ref_code",
                "created_at",
                "confirm_order",
                "payment_status",
            )
        else:
            return ("ref_code", "created_at", "status", "payment_status")

    def confirm_order(self, obj):
        if obj.status == "confirmed":
            url = reverse("book-shipment", args=[obj.pk])
            return format_html('<a href="{}">Book Shipment</a>', url)
        elif obj.status == "pending":
            url = reverse("confirm-order", args=[obj.pk])
            return format_html('<a href="{}">Confirm Order</a>', url)
        elif obj.status == "shipping":
            return "Shipping"
        elif obj.status == "complete":
            return "Complete"
        elif obj.status == "refunded":
            return "Refunded"
        elif obj.status == "returned":
            return "Returned"
        else:
            return "-"


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderShipping)
admin.site.register(ReturnOrder)
admin.site.register(ReturnImage)
admin.site.register(RefundOrder)
