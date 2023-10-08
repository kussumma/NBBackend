from django.contrib import admin

from .models import BlogCategory, BlogTag, Blog, BlogImage, BlogVideo, BlogComment


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 0


class BlogVideoInline(admin.TabularInline):
    model = BlogVideo
    extra = 0


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at", "updated_at", "status")
    list_filter = ("category", "author", "status")
    inlines = [BlogImageInline, BlogVideoInline]
    search_fields = ("title", "content")
    ordering = ("-created_at",)


admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImage)
admin.site.register(BlogVideo)
admin.site.register(BlogComment)
