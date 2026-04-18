from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_mentor', 'is_investor', 'created_at')
    list_filter = ('is_mentor', 'is_investor', 'created_at')
    search_fields = ('username', 'email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
