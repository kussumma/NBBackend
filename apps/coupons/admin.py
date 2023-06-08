from django.contrib import admin

from .models import DiscountType, Coupon, CouponUser, Promo, PromoBanner

admin.site.register(DiscountType)
admin.site.register(Coupon)
admin.site.register(CouponUser)
admin.site.register(Promo)
admin.site.register(PromoBanner)
