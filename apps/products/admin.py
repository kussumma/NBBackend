from django.contrib import admin
from django.db.models import Count

from .models import (
    Category,
    Product,
    Subcategory,
    Subsubcategory,
    Brand,
    Rating,
    Wishlist,
    Stock,
    ExtraProductImage,
)


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0


class ExtraProductImageInline(admin.StackedInline):
    model = ExtraProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "subcategory",
        "subsubcategory",
        "brand",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_filter = ("category", "subcategory", "subsubcategory", "brand", "is_active")
    inlines = [StockInline, ExtraProductImageInline]
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    autocomplete_fields = ("category", "subcategory", "subsubcategory", "brand")


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "size",
        "color",
        "other",
        "quantity",
        "created_at",
        "updated_at",
    )
    list_filter = ("product", "size", "color", "other")
    search_fields = ("product", "size", "color", "other")
    ordering = ("-created_at",)
    autocomplete_fields = ("product",)


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SubcategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SubsubcategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class BrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class WishlistAdmin(admin.ModelAdmin):
    change_list_template = "admin/wishlist_report.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        response.context_data["summary"] = list(
            qs.values(
                "product__id",
                "product__name",
                "product__category__name",
                "product__brand__name",
            )
            .annotate(total=Count("product"))
            .order_by("-total", "product__name")
        )
        return response


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Subsubcategory, SubsubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Rating)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(ExtraProductImage)
