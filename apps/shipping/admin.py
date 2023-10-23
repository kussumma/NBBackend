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
    list_display = ("code", "city", "route", "is_city")
    list_filter = ("is_city",)
    search_fields = ("code", "city", "route")


class ShippingGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


class ShippingGroupItemAdmin(admin.ModelAdmin):
    list_display = ("shipping_group", "shipping_route", "created_at", "updated_at")
    list_filter = ("shipping_group", "shipping_route")
    search_fields = ("shipping_group__name", "shipping_route__route")
    autocomplete_fields = ("shipping_route",)


class ShippingGroupTariffAdmin(admin.ModelAdmin):
    list_display = ("shipping_group", "created_at", "updated_at")
    list_filter = ("shipping_group",)
    search_fields = ("shipping_group__name",)
    autocomplete_fields = ("shipping_group",)


class ShippingAdmin(admin.ModelAdmin):
    list_display = (
        "receiver_name",
        "receiver_phone",
        "receiver_address",
        "destination",
        "created_at",
        "updated_at",
        "is_default",
    )
    list_filter = ("is_default", "created_at", "updated_at")
    search_fields = ("receiver_name", "receiver_phone", "receiver_address")


admin.site.register(ShippingRoute, ShippingRouteAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(ShippingGroup, ShippingGroupAdmin)
admin.site.register(ShippingGroupItem, ShippingGroupItemAdmin)
admin.site.register(ShippingGroupTariff, ShippingGroupTariffAdmin)
admin.site.register(ShippingType)
