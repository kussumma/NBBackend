from django.contrib import admin
from django.forms import ModelForm
from tools.fileupload_helper import FileUploadHelper

from .models import DiscountType, Coupon, CouponUser, Promotion


class CouponFormAdmin(ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()


class PromotionFormAdmin(ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"

    def clean(self):
        if self.cleaned_data.get("cover") == self.instance.cover:
            pass
        else:
            new_cover = self.cleaned_data.get("cover")
            self.cleaned_data["cover"] = FileUploadHelper(
                new_cover, webp=True
            ).validate()
        if self.cleaned_data.get("cover_mobile") == self.instance.cover_mobile:
            pass
        else:
            new_cover_mobile = self.cleaned_data.get("cover_mobile")
            self.cleaned_data["cover_mobile"] = FileUploadHelper(
                new_cover_mobile, webp=True
            ).validate()


class CouponUserInline(admin.TabularInline):
    model = CouponUser
    extra = 0


class CouponAdmin(admin.ModelAdmin):
    form = CouponFormAdmin
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


class PromotionAdmin(admin.ModelAdmin):
    form = PromotionFormAdmin
    list_filter = ("name", "is_active", "valid_from", "valid_to")
    search_fields = ("name", "coupon_code", "description")
    list_display = ("name", "coupon_code", "is_active", "valid_from", "valid_to")
    ordering = ("-created_at",)


admin.site.register(Coupon, CouponAdmin)
admin.site.register(DiscountType)
admin.site.register(CouponUser)
admin.site.register(Promotion, PromotionAdmin)
