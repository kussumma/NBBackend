from django.contrib import admin

from .models import ShippingType, ShippingRoute, ShippingRoutePerType, ShippingCommodity, Shipping

admin.site.register(ShippingType)
admin.site.register(ShippingRoute)
admin.site.register(ShippingRoutePerType)
admin.site.register(ShippingCommodity)
admin.site.register(Shipping)
