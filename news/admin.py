from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import NewsItem, Comment, Bookmark , Category # your models

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_verified',)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('is_verified',)}),
    )



admin.site.register(NewsItem)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Category)


