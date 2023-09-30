from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    ReturnOrder,
    ReturnImage,
    RefundOrder,
    OrderShipping,
)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderShipping)
admin.site.register(ReturnOrder)
admin.site.register(ReturnImage)
admin.site.register(RefundOrder)
