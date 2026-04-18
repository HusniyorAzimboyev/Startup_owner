from django.contrib import admin
from .models import ProgressMetric, Milestone, DailyProgress


@admin.register(ProgressMetric)
class ProgressMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'current_value', 'target_value', 'metric_type')
    list_filter = ('metric_type', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'target_date', 'importance')
    list_filter = ('status', 'importance', 'target_date')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'tasks_completed', 'tasks_total', 'completion_rate')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'date'
    fieldsets = (
        ('User & Date', {
            'fields': ('user', 'date')
        }),
        ('Statistics', {
            'fields': ('tasks_completed', 'tasks_total')
        }),
        ('Note', {
            'fields': ('note',)
        }),
    )
