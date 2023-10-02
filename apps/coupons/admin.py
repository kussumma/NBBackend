from django.contrib import admin

from .models import DiscountType, Coupon, CouponUser, CouponBanner

admin.site.register(DiscountType)
admin.site.register(CouponUser)
admin.site.register(CouponBanner)


class CouponAdmin(admin.ModelAdmin):
    list_filter = ("is_private", "is_limited", "valid_from", "valid_to")
    search_fields = ("prefix_code", "name")


admin.site.register(Coupon, CouponAdmin)
