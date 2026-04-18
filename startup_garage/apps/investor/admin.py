from django.contrib import admin
from .models import Investor, Investment, PitchDeck, InvestorMeeting


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user', 'investment_range', 'verified', 'created_at')
    list_filter = ('investment_range', 'verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('investor', 'startup_founder', 'amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('investor__user__username', 'startup_founder__username')


@admin.register(PitchDeck)
class PitchDeckAdmin(admin.ModelAdmin):
    list_display = ('user', 'version', 'status', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Pitch Deck Info', {
            'fields': ('version', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvestorMeeting)
class InvestorMeetingAdmin(admin.ModelAdmin):
    list_display = ('investor_name', 'user', 'meeting_date', 'status', 'created_at')
    list_filter = ('status', 'meeting_date', 'created_at')
    search_fields = ('investor_name', 'user__username', 'company')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Investor Info', {
            'fields': ('investor_name', 'company')
        }),
        ('Meeting Details', {
            'fields': ('meeting_date', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
