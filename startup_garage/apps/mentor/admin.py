from django.contrib import admin
from .models import Mentor, MentorSession, MentorFeedback


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'availability', 'verified', 'created_at')
    list_filter = ('availability', 'verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MentorSession)
class MentorSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'mentee', 'status', 'scheduled_at')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('title', 'mentor__user__username')


@admin.register(MentorFeedback)
class MentorFeedbackAdmin(admin.ModelAdmin):
    list_display = ('mentor_name', 'user', 'session_date', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'session_date', 'created_at')
    search_fields = ('mentor_name', 'user__username', 'comment')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Session Info', {
            'fields': ('user', 'mentor_name', 'session_date')
        }),
        ('Feedback Content', {
            'fields': ('comment', 'recommendation', 'next_step')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
