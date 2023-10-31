from django.contrib import admin

from .models import DiscountType, Coupon, CouponUser, Promotion


class CouponUserInline(admin.TabularInline):
    model = CouponUser
    extra = 0


class CouponAdmin(admin.ModelAdmin):
    list_filter = ("is_private", "is_limited", "valid_from", "valid_to")
    search_fields = ("prefix_code", "name", "discount_type__name", "discount_value")
    inlines = [CouponUserInline]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                "name",
                "prefix_code",
                "private_decoded",
                "full_code",
                "discount_type",
                "discount_value",
            )
        else:
            return (
                "name",
                "prefix_code",
                "discount_type",
                "discount_value",
            )

    def private_decoded(self, obj):
        return obj.decode_coupon_code(obj.code)

    def full_code(self, obj):
        return obj.prefix_code + obj.decode_coupon_code(obj.code)


admin.site.register(Coupon, CouponAdmin)
admin.site.register(DiscountType)
admin.site.register(CouponUser)
admin.site.register(Promotion)
