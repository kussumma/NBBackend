from django.contrib import admin

from .models import DiscountType, Coupon, CouponUser

admin.site.register(DiscountType)
admin.site.register(Coupon)
admin.site.register(CouponUser)
