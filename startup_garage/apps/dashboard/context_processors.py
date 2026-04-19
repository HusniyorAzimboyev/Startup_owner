from django.utils import timezone
from datetime import datetime
from .models import StartupProfile


def startup_context(request):
    """Add startup info to all templates"""
    context = {
        'startup_name': None,
        'startup_stage': None,
        'days_since_startup': None,
    }
    
    if request.user.is_authenticated:
        try:
            startup = StartupProfile.objects.get(user=request.user)
            context['startup_name'] = startup.name
            context['startup_stage'] = startup.get_stage_display()
            
            # Calculate days since startup
            if startup.created_at:
                delta = timezone.now().date() - startup.created_at.date()
                context['days_since_startup'] = delta.days + 1  # +1 so day 1 = creation day
        except StartupProfile.DoesNotExist:
            pass
    
    return context
