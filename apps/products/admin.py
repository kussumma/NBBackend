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
    ExtraProductVideo,
)

from .admin_views import (
    CategoryFormAdmin,
    SubcategoryFormAdmin,
    SubsubcategoryFormAdmin,
    BrandFormAdmin,
    ProductFormAdmin,
    StockFormAdmin,
    ExtraProductImageFormAdmin,
    ExtraProductVideoFormAdmin,
    RatingFormAdmin,
)


class StockInline(admin.StackedInline):
    form = StockFormAdmin
    model = Stock
    extra = 0


class ExtraProductImageInline(admin.StackedInline):
    form = ExtraProductImageFormAdmin
    model = ExtraProductImage
    extra = 0


class ExtraProductVideoInline(admin.StackedInline):
    form = ExtraProductVideoFormAdmin
    model = ExtraProductVideo
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    form = ProductFormAdmin
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
    inlines = [StockInline, ExtraProductImageInline, ExtraProductVideoInline]
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    autocomplete_fields = ("category", "subcategory", "subsubcategory", "brand")


class StockAdmin(admin.ModelAdmin):
    form = StockFormAdmin
    list_display = (
        "product",
        "size",
        "color",
        "variant",
        "quantity",
        "created_at",
        "updated_at",
    )
    list_filter = ("product", "size", "color", "variant")
    search_fields = ("product", "size", "color", "variant")
    ordering = ("-created_at",)
    autocomplete_fields = ("product",)


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryFormAdmin
    search_fields = ("name",)


class SubcategoryAdmin(admin.ModelAdmin):
    form = SubcategoryFormAdmin
    search_fields = ("name",)


class SubsubcategoryAdmin(admin.ModelAdmin):
    form = SubsubcategoryFormAdmin
    search_fields = ("name",)


class BrandAdmin(admin.ModelAdmin):
    form = BrandFormAdmin
    search_fields = ("name",)


class WishlistAdmin(admin.ModelAdmin):
    change_list_template = "admin/wishlist_report.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context={
                "title": "Wishlist Report",
            },
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


class RatingAdmin(admin.ModelAdmin):
    form = RatingFormAdmin
    list_display = (
        "user",
        "product",
        "star",
        "created_at",
        "updated_at",
    )
    list_filter = ("user", "star")
    search_fields = ("user", "product__name", "star")
    ordering = ("-created_at",)
    autocomplete_fields = ("user", "product")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Subsubcategory, SubsubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(ExtraProductImage)
admin.site.register(ExtraProductVideo)
