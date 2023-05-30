from django.contrib import admin

from .models import User, UserDetail

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login', 'last_updated']

admin.site.register(UserDetail)