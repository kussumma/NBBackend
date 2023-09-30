from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    ShippingRoute,
    Shipping,
    ShippingGroup,
    ShippingGroupItem,
    ShippingGroupTariff,
    ShippingType,
)


class ShippingRouteResource(resources.ModelResource):
    class Meta:
        model = ShippingRoute
        fields = ("code", "city", "route", "is_city")
        import_id_fields = ("code", "city", "route")


class ShippingRouteAdmin(ImportExportModelAdmin):
    resource_classes = [ShippingRouteResource]


admin.site.register(ShippingRoute, ShippingRouteAdmin)
admin.site.register(Shipping)
admin.site.register(ShippingGroup)
admin.site.register(ShippingGroupItem)
admin.site.register(ShippingGroupTariff)
admin.site.register(ShippingType)
