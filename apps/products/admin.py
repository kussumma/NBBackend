from django.contrib import admin

from .models import Category, Product, Subcategory, Brand, Rating, Stock

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(Brand)
admin.site.register(Rating)
admin.site.register(Stock)