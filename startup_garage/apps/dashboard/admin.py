from django.contrib import admin
from .models import StartupProfile


@admin.register(StartupProfile)
class StartupProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'stage', 'kpi_users', 'kpi_revenue', 'created_at')
    list_filter = ('stage', 'created_at')
    search_fields = ('user__username', 'name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User & Basic Info', {
            'fields': ('user', 'name', 'stage')
        }),
        ('KPIs', {
            'fields': ('kpi_users', 'kpi_revenue', 'kpi_traction')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

