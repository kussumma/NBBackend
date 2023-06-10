from django.contrib import admin

from .models import BlogCategory, BlogTag, Blog, BlogImage, BlogVideo, BlogComment

admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(Blog)
admin.site.register(BlogImage)
admin.site.register(BlogVideo)
admin.site.register(BlogComment)
