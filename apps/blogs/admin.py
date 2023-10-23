from django.contrib import admin

from .models import (
    BlogCategory,
    BlogTag,
    Blog,
    BlogImage,
    BlogVideo,
    BlogComment,
    BlogUrl,
)


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 0


class BlogVideoInline(admin.TabularInline):
    model = BlogVideo
    extra = 0


class BlogUrlInline(admin.TabularInline):
    model = BlogUrl
    extra = 0


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at", "updated_at", "status")
    list_filter = ("category", "author", "status")
    inlines = [BlogImageInline, BlogVideoInline, BlogUrlInline]
    search_fields = ["title", "content", "category__name", "author__email"]
    ordering = ("-created_at",)
    autocomplete_fields = ("author",)


admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImage)
admin.site.register(BlogVideo)
admin.site.register(BlogComment)
admin.site.register(BlogUrl)
