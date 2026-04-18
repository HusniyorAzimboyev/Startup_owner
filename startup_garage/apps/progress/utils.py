from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import DailyProgress
from apps.tasks.models import Task


def calculate_streak(user):
    """
    Calculate consecutive days with at least 1 task completed.
    
    Args:
        user: User object
        
    Returns:
        int: Current streak count
    """
    streak = 0
    today = timezone.now().date()
    
    # Get all daily progress entries for user ordered by date descending
    entries = DailyProgress.objects.filter(user=user).order_by('-date')
    
    for entry in entries:
        # Start from today and work backwards
        expected_date = today - timedelta(days=streak)
        
        # If there's a gap, break the streak
        if entry.date != expected_date:
            break
            
        # Only count if at least 1 task was completed
        if entry.tasks_completed > 0:
            streak += 1
        else:
            break
    
    return streak


def sync_daily_progress(user):
    """
    Sync daily progress with current task counts.
    Creates or gets today's entry and updates task counts from Task model.
    
    Args:
        user: User object
        
    Returns:
        DailyProgress: Today's progress entry
    """
    today = timezone.now().date()
    
    # Get or create today's entry
    progress, created = DailyProgress.objects.get_or_create(
        user=user,
        date=today
    )
    
    # Get task counts from Task model
    user_tasks = Task.objects.filter(user=user)
    progress.tasks_total = user_tasks.count()
    progress.tasks_completed = user_tasks.filter(status='done').count()
    progress.save()
    
    return progress
