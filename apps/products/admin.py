from django.contrib import admin

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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Subsubcategory, SubsubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Rating)
admin.site.register(Wishlist)
admin.site.register(Stock, StockAdmin)
admin.site.register(ExtraProductImage)
