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
)


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "subcategory",
        "subsubcategory",
        "brand",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_filter = ("category", "subcategory", "subsubcategory", "brand", "is_active")
    inlines = [StockInline]
    search_fields = ("name", "sku", "description")
    ordering = ("-created_at",)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory)
admin.site.register(Subsubcategory)
admin.site.register(Brand)
admin.site.register(Rating)
admin.site.register(Wishlist)
admin.site.register(Stock)
