from django.contrib import admin

from .models import Category, Product, Subcategory, Tag, Brand, Rating, Wishlist, Stock

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(Tag)
admin.site.register(Brand)
admin.site.register(Rating)
admin.site.register(Wishlist)
admin.site.register(Stock)